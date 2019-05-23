#from msbwtCloud import MultiStringBWTCloud 
import MultiStringBWTCloud as MultiStringBWTCloud
testHost = 'http://nvnano.cs.unc.edu:8080'
msbwt = MultiStringBWTCloud.loadBWTCloud(testHost)

def test_countOccurrencesOfSeq():
    res = msbwt.countOccurrencesOfSeq('TAA')
    print(res['result'])

def test_countOccurrencesOfSeq_givenRange():
    print msbwt.countOccurrencesOfSeq('T', (1346091641L, 15700916349L)) == 2652271619

def test_countOccurrencesOfSeq_givenRange_keyword():
    print msbwt.countOccurrencesOfSeq('T', givenRange=(1346091641L, 15700916349L)) == 2652271619

def test_findIndicesOfStr():
    print msbwt.findIndicesOfStr('AA') == (1346091641L, 15700916349L)

def test_findIndicesOfStr_givenRange():
    print msbwt.findIndicesOfStr('T', (1346091641L, 15700916349L)) == (108900066278L, 111552337897L)

def test_findIndicesOfStr_givenRange_keyword():
    print msbwt.findIndicesOfStr('T', givenRange=(1346091641L, 15700916349L)) == (108900066278L, 111552337897L)

def test_getSequenceDollarID():
    print msbwt.getSequenceDollarID(15700916349) == 763

def test_getSequenceDollarID_returnOffset():
    print msbwt.getSequenceDollarID(15700916349, True) == (763L, 149L)

def test_getSequenceDollarID_returnOffset_keyword():
    print msbwt.getSequenceDollarID(15700916349, returnOffset=True) == (763L, 149L)

def test_recoverString():
    print msbwt.recoverString(15700916349) == "AC$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

def test_batchRecoverString():
    print msbwt.batchRecoverString((15700916349,15700916351)) == ['AC$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'AC$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAACACAACAGACACACC']

