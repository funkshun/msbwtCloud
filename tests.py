import msbwtCloud.MultiStringBWTCloud as msb
import json
import os
import requests
def main():
    
    msbwt = msb.loadBWTCloud('http://nvnano.cs.unc.edu:8080')
    res = msbwt.countOccurrencesOfSeq(u'T')['result']
    print(res)

# def main():
#     r = requests.get('http://nvnano.cs.unc.edu:8080/checkAlive?args=[]')
#     j = r.json()
#     print(j)

if __name__ == '__main__':
    main()