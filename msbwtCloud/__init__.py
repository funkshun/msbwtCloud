import os
import json
import sys
import requests
import ast
import datetime as dt
import time
import sqlite3
from msbwtCloud.db import *
import secrets
import string
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread
from MUSCython import MultiStringBWTCython as MSBWT
from msbwtCloud.fastBatchKmerCounter import generate_counts as fastBatchKmerCounts
from concurrent.futures import ThreadPoolExecutor



def create_app(test_config=None):

    """
        Flask Boilerplate
    """
    DEBUG = True

    app = Flask(__name__, instance_relative_config = True)
    
    app.config.from_object('msbwtCloud.config')

    create_db(app.config['DB_ROOT'])

    executor = ThreadPoolExecutor(max_workers=app.config['QUERY_WORKERS'])
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    """
        BWT Configuration, should be moved to config file
    """
    
    #app.config['BWT'] = MSBWT.loadBWT(app.config['BWT_ROOT'])
    
    results_lst = {}
    
    #app.config['scheduler'] = BackgroundScheduler()
    #app.config['scheduler'].add_job(_cleanQueries, 'interval', minutes=20)
    #app.config['scheduler'].add_job(_cleanQueriesDB, 'interval', minutes=20)

    @app.route('/checkAlive')
    def checkAlive():
        names = []
        for filename in os.listdir(app.config['BWT_ROOT']):
            try:
                bwt = MSBWT.loadBWT(app.config['BWT_ROOT'] + filename)
                if bwt.countOccurrencesOfSeq('T'.encode('utf-8', 'ignore')) > 0:
                    names.append(filename.decode('utf-8'))
                else:
                    continue
            except Exception as e:
                print(e)
                continue
        data = {"names":names}
        return Response(json.dumps(data), status=200)

    # @app.route('/<func_call>')
    # def functionCallerLegacy(func_call):
    #     bwt = MSBWT.loadBWT(app.config['BWT_ROOT'] + 'CC027M756_UNC_NYGC/'.encode('utf-8', 'ignore'))

    #     args = ast.literal_eval(request.args.get('args', None))
    #     kwargs = request.args.get('kwargs', None)
    #     if args is None:
    #         return Response(status=400)

    #     if kwargs is not None:
    #         kwargs = ast.literal_eval(kwargs)

    #     else:
    #         kwargs = {}
    #         ar = [func_call, args, kwargs, bwt]
    #         r = executor.submit(_runLegacy, *ar)
    #         return Response(json.dumps({'result': r.result()}), status=200)


    """
        Primary Function Route
        Accepts connections bearing the name of a functioon and the corresponding
        arguments in the form ?args=[...]
        Accepted Functions:
        -countOccurrencesOfSeq
        -recoverString

    """
    @app.route('/<name>/<func_call>')
    def functionCaller(name, func_call):
        
        if DEBUG:
            print("Serving {}".format(name))
        
        bwt = MSBWT.loadBWT(app.config['BWT_ROOT'] + name.encode('utf-8', 'ignore') + '/'.encode('utf-8', 'ignore'))

        args = ast.literal_eval(request.args.get('args', None))
        kwargs = request.args.get('kwargs', None)
        async_flag = request.args.get('async', None)

        if args is None:
            return Response(status=400)
        if kwargs is not None:
            kwargs = ast.literal_eval(kwargs)
        else:
            kwargs = {}

        #Legacy Compatibility, disable non-blocking functionality
        if async_flag is None or async_flag.lower() == 'false':
            ar = [func_call, args, kwargs, bwt]
            r = executor.submit(_runLegacy, *ar)
            return Response(json.dumps({'result': r.result()}), status=200)

        tok = getToken()
        st = 405
        try:
            results_lst[tok] = {}
            ar = [func_call, args, kwargs, bwt, tok]
            executor.submit(_run, *ar)
            results_lst[tok]['func'] = func_call
            results_lst[tok]['args'] = args
            results_lst[tok]['kwargs'] = kwargs
            st = 200
        except:
            st = 405
        summary = {
            'data': app.config['DATA'],
            'name': name,
            'token': tok,
            'function': func_call,
            'args': args,
            'kwargs': kwargs
        }
        return Response(json.dumps(summary), status=st)

    #Retrieves the results of a query based on a transaction token
    @app.route('/results/<token>')
    def results(token):

        # Retrieve Token status from Results
        try:
            # token = token.encode('ascii', 'ignore')
            j = retrieve_token(connect_db(app.config['DB_ROOT']), token)
            data = {'result': j['result'], 
                    'date': j['date'], 
                    'status': j['status'],
                    'function': j['func'],
                    'args': j['args'],
                    'kwargs': j['kwargs'],
                    'data': app.config['DATA']}
            
            return Response(json.dumps(data), status = 200)

        #Token Not Found        
        except Exception as e:
            print(e)
            return Response(str(e), status = 404)

    @app.route('/purge')
    def purge():
        purge_db(connect_db(app.config['DB_ROOT']))
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
            args_b = [a.encode('utf-8', 'ignore') for a in args]
            # Handles Basic BWT functions
            if func_call in available:
                f = getattr(bwt, func_call)
                result = f(*args_b, **kwargs)
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

            results_lst[token]['status'] = 'SUCCESS'
            results_lst[token]['done'] = True

        except Exception as e:
            results_lst[token]['result'] = 'No Result'
            results_lst[token]['status'] = 'FAILED'
            results_lst[token]['done'] = True
            print(e)

        insert_task(connect_db(app.config['DB_ROOT']), 
                            token, 
                            results_lst[token], 
                            results_lst[token]['date'].strftime("%Y-%m-%d, %H:%M:%S"))
        del results_lst[token]

        return


    def _runLegacy( func_call, args, kwargs, bwt):

        """
            Initializes Job entry in Result List.
        """
        try:  
            
            available = dir(bwt)
            args_b = [a.encode('utf-8', 'ignore') if isinstance(a, str) else a for a in args]
            # Handles Basic BWT functions
            if func_call in available:
                f = getattr(bwt, func_call)
                result = f(*args_b, **kwargs)
                
                
            # Recovers all strings from range of indices, non-parallel
            elif func_call == 'batchRecoverString':
                recoverStrings = []
                for index in range(args[0][0], args[0][1]):
                    recoverStrings.append(bwt.recoverString(index).decode('utf-8'))
                result = recoverStrings
            
            #Batch Sequence Counts, non parallel
            elif func_call == 'batchCountOccurrencesOfSeq':
                counts = []
                for seq in args:
                    counts.append(bwt.countOccurrencesOfSeq(seq))
                result = counts

            # Optimized Occurrence Count
            elif func_call == 'batchFastCountOccurrencesOfSeq':
                result = fastBatchKmerCounts(bwt, args)

            return result

        except Exception as e:
            print(e)
            return None

        return result
       
    return app

def getToken():
    alphabet = string.ascii_letters + string.digits
    t = ""
    for i in range(15):
        t = t + secrets.choice(alphabet)
    return t
