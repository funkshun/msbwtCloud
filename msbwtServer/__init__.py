import os
import json
import sys
import MultiStringBWTCloud as msb
import requests
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing.pool import ThreadPool
def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'msbwt.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(checkHosts, 'interval', minutes=5)
    alive, bwts = checkHosts()


    @app.route('/')
    def index():
        return render_template('index.html', res=bwts)

    @app.route('/hosts')
    def listHosts():
        return Response(json.dumps(alive), status=200)
    
    @app.route('/<func_call>')
    def functionCaller(func_call):
        if func_call == 'functons':
            return render_template('functions.html', name=name)
        else:
            
            args = request.args.get('args', None).encode('ascii', 'ignore')
            names = [x.encode('ascii', 'ignore') for x in request.args.getlist('names')]
            
            pool = ThreadPool(processes = 2)
            rets = []
            for i, name in enumerate(names):
                rets.append(pool.apply_async(makeRequest, (name, func_call, args, bwts)))
            for i, a in enumerate(rets):
                rets[i] = a.get()
            return render_template('result.html', func_call=func_call, res=rets, ar=args)
        #return r.json()


    return app

def checkHosts():
        ROOT = os.path.realpath(os.path.dirname(__file__))
        try:
            with open(os.path.join(ROOT, 'hosts'), 'r') as f:
                host_lst = f.read()
            hosts = [x.strip() for x in host_lst.split("\n")]
            #print(hosts)
        except Exception as e:
            print("Error opening hosts file. Ensure file exists and is populated")
            print(e)
            sys.exit(1)

        alive = {}
        for h in hosts:
            try:
                r = requests.get('http://' + h + '/checkAlive?args=[]')
                j = r.json()
                #print(j)
                if(j['alive']):
                    #print(j)
                    alive[h] = j
                bwts = {}
                for key in alive.keys():
                    #bwts[alive[key]['name']] = msb.loadBWTCloud('http://' + key)
                    bwts[alive[key]['name']] = 'http://' + key

            except:
                pass
        return (alive, bwts)

def makeRequest(name, func, args, maps):
    target = maps[name]
    para = {
                'args' : args
    }
    r = requests.get(target + '/' + func, params = para)
    return r.json()


    


    
