import os
import json
import sys
import requests
import ast
#import secrets
import random
import string
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing.pool import ThreadPool
from MUSCython import MultiStringBWTCython as MSBWT


def create_app(test_config=None):

    """
        Flask Boilerplate
    """

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


    """
        BWT Configuration, should be moved to config file
    """
    app.config['BWT_ROOT'] = '/opt/msbwt/CC027M756_UNC_NYGC/'
    app.config['BWT'] = MSBWT.loadBWT(app.config['BWT_ROOT'])
    app.config['data'] = {
        'name': app.config['BWT_ROOT'].strip().split("/").strip()[-2],
        'description': "",
        'load': 0
    }
    
    
    

    

    @app.route('/<func_call>')
    def functionCaller(func_call):
        if func_call == 'checkAlive':
            try:
                if app.config['BWT'].countOccurrencesOfSeq('T') > 0:
                    return Response(json.dump(app.config['data']), status=200)
                else:
                    return Response(status=500)
            except:
                return Response(status=500)

        else:
            args = request.args.get('args', None)
            if args is None:
                return Response(status=400)
            available = dir(app.config['BWT'])
            # positional arguments
            args = ast.literal_eval(args.encode('utf-8'))
            # keyword arguments
            kwargs = {}
            tok = getToken()
            st = 405
            if func_call in available:
                f = getattr(app.config['BWT'], func_call)
                waiting[tok] = (f, args, kwargs)
                st = 200
            summary = {
                'data': app.config['data'],
                'token': tok,
                'function': func_call,
                'args': args,
                'kwargs': kwargs
            }
            return Response(json.dump(summary), status=st)
            
            
    return app

def getToken():
    alphabet = string.ascii_letters + string.digits
    t = ""
    for i in range(15):
        t = t + random.choice(alphabet)
    return t
            
            
    

    

        



    


