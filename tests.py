import msbwtCloud.MultiStringBWTCloud as msb
import json
import os
# def main():
    
#     msbwt = msb.loadBWTCloud('http://nvnano.cs.unc.edu:8080')
#     res = msbwt.countOccurrencesOfSeq('T')['result']
#     print(type(res))

def main():
    print json.dumps({'alive': True, 'name': os.path.dirname(__file__)})

if __name__ == '__main__':
    main()