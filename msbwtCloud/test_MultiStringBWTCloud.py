from msbwtCloud import MultiStringBWTCloud 

testHost = 'http://csbio-desktop008.cs.unc.edu:8080'
msbwt = MultiStringBWTCloud.loadBWTCloud(testHost)

def test_countOccurrencesOfSeq():
    assert msbwt.countOccurrencesOfSeq('TAA') == 2652271619

def test_countOccurrencesOfSeq_givenRange():
    assert msbwt.countOccurrencesOfSeq('T', (1346091641L, 15700916349L)) == 2652271619

def test_countOccurrencesOfSeq_givenRange_keyword():
    assert msbwt.countOccurrencesOfSeq('T', givenRange=(1346091641L, 15700916349L)) == 2652271619

def test_findIndicesOfStr():
    assert msbwt.findIndicesOfStr('AA') == (1346091641L, 15700916349L)

def test_findIndicesOfStr_givenRange():
    assert msbwt.findIndicesOfStr('T', (1346091641L, 15700916349L)) == (108900066278L, 111552337897L)

def test_findIndicesOfStr_givenRange_keyword():
    assert msbwt.findIndicesOfStr('T', givenRange=(1346091641L, 15700916349L)) == (108900066278L, 111552337897L)

def test_getSequenceDollarID():
    assert msbwt.getSequenceDollarID(15700916349) == 763

def test_getSequenceDollarID_returnOffset():
    assert msbwt.getSequenceDollarID(15700916349, True) == (763L, 149L)

def test_getSequenceDollarID_returnOffset_keyword():
    assert msbwt.getSequenceDollarID(15700916349, returnOffset=True) == (763L, 149L)

def test_recoverString():
    assert msbwt.recoverString(15700916349) == "AC$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

def test_batchRecoverString():
    assert msbwt.batchRecoverString((15700916349,15700916351)) == ['AC$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'AC$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAACACAACAGACACACC']

