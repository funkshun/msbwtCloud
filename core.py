import cherrypy
import pysam
import MUSCython
from MUSCython import MultiStringBWTCython as MSBWT
import time
import ast
import sys

@cherrypy.popargs('func_call')
class BWTQuery(object):
    
    def __init__(self):
        self.msbwt = MSBWT.loadBWT(sys.argv[1])

    @cherrypy.expose()
    def index(self, func_call, **params):
        available = dir(self.msbwt)
        # positional arguments
        args = params.get('args')
        args = ast.literal_eval(args.encode('utf-8'))
        # keyword arguments
        kwargs = {}
        for key,val in params.iteritems():
            if key == 'args':
                continue
            kwargs[key]=ast.literal_eval(val.encode('utf-8'))
        if func_call in available:
            f = getattr(self.msbwt, func_call)
            cherrypy.response.status = 202
            result = f(*args, **kwargs)
            cherrypy.response.status = 200
            # TODO: make sure repr doesn't break anything (sometimes can return class name, etc) 
            return repr(result)
        elif func_call == 'batchRecoverString':
            print args
            return repr(self.batchRecoverStringFunc(*args))
        elif func_call == 'batchCountOccurrencesOfSeq':
            print args
            return repr(self.batchCountOccurrencesOfSeqFunc(*args))
        else:
            raise cherrypy.HTTPError(405, "MSBWT method not found.")

    def batchRecoverStringFunc(self, (startIndex, endIndex)):
        recoverStrings = []
        for index in range(startIndex, endIndex):
            recoverStrings.append(self.msbwt.recoverString(index))
        return recoverStrings

    def batchCountOccurrencesOfSeqFunc(self, queries):
        counts = []
        for q in queries:
            counts.append(self.msbwt.countOccurrencesOfSeq(q))
        return counts


if __name__=='__main__':
    cherrypy.config.update(
            {'server.socket_host': '0.0.0.0',
             'server.socket_port': 8080})
    cherrypy.quickstart(BWTQuery())
