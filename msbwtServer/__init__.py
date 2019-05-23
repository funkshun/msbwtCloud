import os
import json
import sys
import MultiStringBWTCloud as msb
from flask import Flask

def create_app(test_config=None):
    try:
        with open('hosts', 'r') as f:
            host_lst = f.read()
        hosts = host_lst.split("\n").trim()
    except:
        print("Error opening hosts file. Ensure file exists and is populated")
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
    for h in hosts:
        print(h)
    


    
