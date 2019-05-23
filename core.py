import cherrypy
import pysam
import MUSCython
from MUSCython import MultiStringBWTCython as MSBWT
import time
import ast
import sys
import json
import os
from fastBatchKmerCounter import generate_counts as fastBatchKmerCounts


@cherrypy.popargs('func_call')
class BWTQuery(object):

    def __init__(self):
        self.msbwt = MSBWT.loadBWT(sys.argv[1])
        # file_data = {}
        # for f in os.listdir(sys.argv[1]):
        #     file_data[f] = os.path.getsize()

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
            return json.dumps({'result':result})
        # TODO: evaluate whether it's better to do these elifs or expose the methods (see batchCount)
        # Note: if expose, need to do the same argument handling (args) as above in each method
        elif func_call == "checkAlive":
            try:
                if self.msbwt.countOccurrencesOfSeq('T') > 0:
                    return json.dumps({'result': True})
                else:
                    return json.dumps({'result': False})
            except:
                return json.dumps({'result': False})
        elif func_call == 'batchRecoverString':
            return json.dumps({'result': self.batchRecoverStringFunc(*args)})
        elif func_call == 'batchCountOccurrencesOfSeq':
            return json.dumps({'result': self.batchCountOccurrencesOfSeqFunc(*args)})
        elif func_call == 'batchFastCountOccurrencesOfSeq':
            return json.dumps({'result': self.batchFastCountOccurrencesFunc(*args)})
        else:
            raise cherrypy.HTTPError(405, "MSBWT method not found.")

    #TODO: raise errors for incorrect paramters
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

    def batchFastCountOccurrencesFunc(self, queries):
        return fastBatchKmerCounts(self.msbwt, queries)



if __name__=='__main__':
    cherrypy.config.update(
            {'server.socket_host': '0.0.0.0',
             'server.socket_port': 8080})
    cherrypy.quickstart(BWTQuery())
