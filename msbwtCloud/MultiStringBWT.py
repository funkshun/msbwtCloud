import pysam
from MUS import MultiStringBWT
import urllib

class MultiStringBWTCloud(MultiStringBWT.BasicBWT):
    '''
    Extend MUS.MultiStringBWT.BasicBWT
    
    Shared Functions:
    __init__
    counstructIndexing
    countOccurrencesOfSeq
    findIndicesOfStr
    getSequenceDollarID
    recoverString

    Override functions:
    loadMsbwt
    constructTotalCounts
    constructFMIndex
    getCharAtIndex
    getBWTRange
    getOccurrenceOfCharAtIndex
    getFullFMAtIndex
    iterInit
    iterNext
    iterNext_cython
    '''

    def __init__(self):
        self.servers = {'C57BL6J_m003636A':'http://csbio-desktop008.cs.unc.edu:8080/'}

    def constructIndexing(self):
        pass

    def countOccurrencesOfSeq(self, seq, givenRange=None):
        '''
        This function counts the number of occurrences of the given sequence 
        @param seq - the sequence to search for
        @param givenRange - the range to start from (if a partial search has already been run), default=whole range
        @return - an integer count of the number of times seq occured in this BWT
        '''
        query = "{}?args=['{}']".format(self.baseServer+'countOccurrencesOfSeq',seq)
        if givenRange != None:
            lo = givenRange[0]
            hi = givenRange[1]
            query += "&givenRange=({},{})".format(lo,hi)
        r = urllib.urlopen(query)
        return r.read()
        
    def findIndicesOfStr(self, seq, givenRange=None):
        query = "{}?args=['{}']".format(self.baseServer+'findIndicesOfStr',seq)
        if givenRagne != None:
            lo = givenRange[0]
            hi = givenRange[1]
            query += "&givenRange=({},{})".format(lo,hi)
        r = urllib.urlopen(query)
        return r.read()

    def getSequenceDollarID(self, strIndex, returnOffset=False):
        pass

    def recoverString(self, strIndex, withIndex=False):
        pass

    def loadMsbwt(self, dirName, logger=None):
        self.dirName = dirName
        self.baseServer = self.servers.get(self.dirName)
        return self.baseServer

    def constructTotalCounts(self, logger):
        pass

    def constructFMIndex(self, logger):
        pass

    def getCharAtIndex(self, index):
        pass

    def getBWTRange(self, start, end):
        pass

    def getOccurrenceOfCharAtIndex(self, sym, index):
        pass

    def getFullFMAtIndex(self, index):
        pass

    def createKmerProfile(self, k, profileCsvFN):
        pass

