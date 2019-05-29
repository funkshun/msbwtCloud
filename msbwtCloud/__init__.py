import os
import json
import sys
import requests
import ast
import datetime as dt
import time
#import secrets
import random
import string
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from apscheduler.schedulers.background import BackgroundScheduler
#from multiprocessing.pool import ThreadPool
from threading import Thread
from MUSCython import MultiStringBWTCython as MSBWT
from fastBatchKmerCounter import generate_counts as fastBatchKmerCounts


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
        'name': app.config['BWT_ROOT'].strip().split("/")[-2].strip(),
        'description': "",
        'load': 0
    }

    
    results_lst = {}
    #pool = ThreadPool(processes=2)
    
    """
        Primary Function Route
        Accepts connections bearing the name of a functioon and the corresponding
        arguments in the form ?args=[...]
        Accepted Functions:
        -countOccurrencesOfSeq
        -recoverString

    """
    @app.route('/<func_call>')
    def functionCaller(func_call):
        if func_call == 'checkAlive':
            try:
                if app.config['BWT'].countOccurrencesOfSeq('T') > 0:
                    return Response(json.dumps(app.config['data']), status=200)
                else:
                    return Response(status=500)
            except:
                return Response(status=500)

        else:
            args = request.args.get('args', None)
            if args is None:
                return Response(status=400)
            
            # positional arguments
            args = ast.literal_eval(args.encode('utf-8'))
            # keyword arguments
            kwargs = {}
            tok = getToken()
            st = 405
            #try:
            results_lst[tok] = {}
            results_lst[tok]['thread'] = Thread(target = _run, args = (func_call, args, kwargs, app.config['BWT'], tok))
            results_lst[tok]['thread'].start()
            results_lst[tok]['func'] = func_call
            results_lst[tok]['args'] = args
            results_lst[tok]['kwargs'] = kwargs
            #tmp = pool.apply_async(_run, args = (func_call, args, kwargs, app.config['BWT'], tok))
            st = 200
            #except:
             #   st = 405
            summary = {
                'data': app.config['data'],
                'token': tok,
                'function': func_call,
                'args': args,
                'kwargs': kwargs
            }
            return Response(json.dumps(summary), status=st)

    @app.route('/results/<token>')
    def results(token):
        try:
            token = token.encode('ascii', 'ignore')
            j = results_lst[token]
            data = {'result': j['result'], 
                    'date': j['date'].strftime("%m/%d/%Y, %H:%M:%S"), 
                    'status': j['status'],
                    'function': j['func'],
                    'args': j['args'],
                    'kwargs': j['kwargs']}
            
            return Response(json.dumps(data), status = 200)
        except Exception as e:
            print(e)
            return Response(status = 404)

    @app.route('/purge')
    def purge():
        results_lst = {}
        return Response(status=200)

    def _run( func_call, args, kwargs, bwt, token):

        """
            Initializes Job entry in Result List.
        """
        results_lst[token] = {}
        results_lst[token]['done'] = False
        results_lst[token]['date'] = dt.datetime.now()
        results_lst[token]['result'] = None
        results_lst[token]['status'] = 'RUNNING'
        try:  
            
            available = dir(bwt)
            
            # Handles Basic BWT functions
            if func_call in available:
                f = getattr(bwt, func_call)
                result = f(*args, **kwargs)
                results_lst[token]['result'] = result
            
            # Long running job for testing non-blocking properties
            elif func_call == 'testr':
                x = int(args[0])
                time.sleep(x)
                results_lst[token]['result'] = "Slept " + str(x) + " seconds"
                
            # Recovers all strings from range of indices, non-parallel
            elif func_call == 'batchRecoverString':
                recoverStrings = []
                for index in range(args[0], args[1] + 1):
                    recoverStrings.append(bwt.recoverString(index))
                results_lst[token]['result'] = recoverStrings
            
            #Batch Sequence Counts, non parallel
            elif func_call == 'batchCountOccurrencesOfSeq':
                counts = []
                for seq in args:
                    counts.append(bwt.countOccurrencesOfSeq(seq))
                results_lst[token]['result'] = counts

            # Optimized Occurrence Count
            elif func_call == 'batchFastCountOccurrencesOfSeq':
                results_lst[token]['result'] = fastBatchKmerCounts(bwt, args)


        except Exception as e:
            results_lst[token]['result'] = e.message
            results_lst[token]['status'] = 'FAILED'
            results_lst[token]['done'] = True
            return

        results_lst[token]['status'] = 'SUCCESS'
        results_lst[token]['done'] = True
        return

            
            
    return app

def getToken():
    alphabet = string.ascii_letters + string.digits
    t = ""
    for i in range(15):
        t = t + random.choice(alphabet)
    return t




    


