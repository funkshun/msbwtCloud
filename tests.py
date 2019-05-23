import msbwtCloud.MultiStringBWTCloud as msb

def main():
    
    msbwt = msb.loadBWTCloud('http://nvnano.cs.unc.edu:8080')
    res = msbwt.countOccurrencesOfSeq('T')['result']
    print(type(res))

if __name__ == '__main__':
    main()