import pysam
from MUS import MultiStringBWT
import urllib


class loadBWTCloud(MultiStringBWT.BasicBWT):
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

    def __init__(self, urlBase):
        if urlBase[-1] != "/":
            urlBase += "/"
        self.urlBase = urlBase

    def __constructQuery(self, funcName, *args, **kwargs):
        argsStr = ''
        for a in args:
            if isinstance(a, str):
                argsStr += "'{}'".format(a)
            else:
                argsStr += str(a)
        queryStr = "{}?args=[{}]".format(self.urlBase+funcName, argsStr)
        for key, val in kwargs.iteritems():
            if val:
                queryStr += "&{}={}".format(key, str(val).replace(" ","")) # remove whitespace from val 
        return queryStr

    def __returnQuery(self, query):
        r = urllib.urlopen(query)
        return eval(r.read())

    def constructIndexing(self):
        pass

    def countOccurrencesOfSeq(self, seq, givenRange=None):
        '''
        Executes countOccurrencesOfSeq query on the msbwt associated with the hostname. See below for msbwt documentation:
        
        This function counts the number of occurrences of the given sequence 
        @param seq - the sequence to search for
        @param givenRange - the range to start from (if a partial search has already been run), default=whole range
        @return - an integer count of the number of times seq occured in this BWT
        '''
        if not givenRange:
            givenRange = {}
        query = self.__constructQuery("countOccurrencesOfSeq", seq, givenRange=givenRange)
        return self.__returnQuery(query)
        
    def findIndicesOfStr(self, seq, givenRange=None):
        '''
        Executes findIndicesOfStr query on the msbwt associated with the hostname. See below for msbwt documentation:

        This function will search for a string and find the location of that string OR the last index less than it. It also
        will start its search within a given range instead of the whole structure
        @param seq - the sequence to search for
        @param givenRange - the range to search for, whole range by default
        @return - a python range representing the start and end of the sequence in the bwt
        '''
        if not givenRange:
            givenRange = {}
        query = self.__constructQuery("findIndicesOfStr", seq, givenRange=givenRange)
        return self.__returnQuery(query)

    def getSequenceDollarID(self, strIndex, returnOffset=False):
        '''
        Executes getSequenceDollarID query on the msbwt associated with the hostname. See below for msbwt documentation:

        This will take a given index and work backwards until it encounters a '$' indicating which dollar ID is
        associated with this read
        @param strIndex - the index of the character to start with
        @return - an integer indicating the dollar ID of the string the given character belongs to
        '''
        query = self.__constructQuery("getSequenceDollarID", strIndex, returnOffset=returnOffset)
        return self.__returnQuery(query)

    def recoverString(self, strIndex, withIndex=False):
        '''
        Executes recoverString query on the msbwt associated with the hostname. See below for msbwt documentation:

        This will return the string that starts at the given index
        @param strIndex - the index of the string we want to recover
        @return - string that we found starting at the specified '$' index
        '''
        query = self.__constructQuery("recoverString", strIndex, withIndex=withIndex)
        return self.__returnQuery(query)

    def constructTotalCounts(self, logger):
        # TODO: reevaluate the assumption below -- need this function?
        # assume this is already done 
        pass

    def constructFMIndex(self, logger):
        # TODO: reevaluate the assumption below
        # assume this is already done
        pass

    def getCharAtIndex(self, index):
        # TODO: evaluate if need this function (only necessary for other functions)
        pass

    def getBWTRange(self, start, end):
        # TODO: evaluate if need this function (only necessary for other functions)
        pass

    def getOccurrenceOfCharAtIndex(self, sym, index):
        # TODO: evaluate if need this function
        pass

    def getFullFMAtIndex(self, index):
        # TODO: evaluate if need this function
        pass

    def createKmerProfile(self, k, profileCsvFN):
        # TODO: evaluate if need this function
        pass

    def batchRecoverString(self, givenRange):
        query = self.__constructQuery("batchRecoverString", givenRange)
        return self.__returnQuery(query)

