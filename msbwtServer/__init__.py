import os
import json
import sys
import MultiStringBWTCloud as msb
import requests
from flask import Flask

def create_app(test_config=None):
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
    alive = {}
    for h in hosts:
        try:
            r = requests.get('http://' + h + '/checkAlive?args=[]')
            j = json.load(r.json())
            if(j['alive']):
                print(j)
                alive[h] = j
        except:
            pass

    @app.route('/hosts')
    def listHosts():
        return json.dumps(alive)

    return app

    


    
