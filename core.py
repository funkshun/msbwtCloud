import cherrypy
import pysam
import MUSCython
from MUSCython import MultiStringBWTCython as MSBWT
import time


@cherrypy.popargs('func_call')
class BWTQuery(object):
    
    def __init__(self):
        self.msbwt = MSBWT.loadBWT('/playpen/C57BL6J_m003636A')

    @cherrypy.expose()
    def index(self, func_call, **params):
        available = dir(self.msbwt)
        if func_call in available:
            f = getattr(self.msbwt, func_call)
            # positional arguments
            args = params.get('args')
            args = eval(args.encode('utf-8'))
            # keyword arguments
            kwargs = {}
            for key,val in params.iteritems():
                if key == 'args':
                    continue
                kwargs[key]=eval(val.encode('utf-8'))
            # 202 response code is Accepted -- accepted for processing, but the processing has not been completed
            # TODO: change based on subprocess status
            cherrypy.response.status = 202
            result = f(*args, **kwargs)
            # time.sleep(60)
            cherrypy.response.status = 200
            # TODO: make sure repr doesn't break anything (sometimes can return class name, etc) 
            return repr(result)
        else:
            print 'Function %s not found in msbwt functions' % func_call
            cherrypy.response.status = 400


if __name__=='__main__':
    cherrypy.config.update(
            {'server.socket_host': '0.0.0.0',
             'server.socket_port': 8080})
    cherrypy.quickstart(BWTQuery())
