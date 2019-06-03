# msBWT Cloud

## msBWT RESTful interface

msbwtCloud provides an RESTful interface for non-blocking requests to a remote msBWT data structure.
Queries return a request token and summary and results can be retrieved by providing the token at the results api endpoint.
This is intended to bypass the issues present in current versions of remote BWT access, namely blocking requests and large IO overhead.
Current implementations rely on transmitting the BWT across a local network to the server assigned to a query, a process which may account for more than 50% of the total request time.
Furthermore, each of these requests blocks until completion preventing the start of additional related queries, a typical use case.
This solves these issues by assigning each BWT to the local storage of a low cost machine,
and by allowing for the acquisition of results based on tokenization rather than a blocking response.
This also trivializes the storage of query results, preventing wasted computational resources on repeated queries.

## Installation

- Clone this repository on to the device hosting the BWT datastructure.
- Change `config.py` values to match desired values
- Run `python setup.py install`
- Run `waitress-serve --call 'msbwtCloud:create_app'` to create server on port 8080

## msBWTCloud

msBWTCloud provides the primary interface for interacting with remote BWT data structures. The following functions are exposed at:

`/<function_name>?args=[args_list]&kwargs={kwargs_list}`

### Status Codes

`202`: Query properly received and queued  
`400`: Improper arguments  
`404`: Function not found

### countOccurrencesOfSeq

Queries the number of times a sequence occurrs in the target dataset.

- Arguments  
    `seq::String`: the target sequence to be counted  
    `givenRange::(Long, Long)`: (OPTIONAL) Restricts the query to the given range
- Sample Call  
`http://test.test/countOccurrencesOfSeq?args=["CATAGAT"]`  
Queries the number of occurrences of `CATAGAT` between
`1346091641L` and `15700916349L` in the dataset held by `test.test`

### recoverString

Queries the string at the index given in the target dataset.

- Arguments  
    `index::Integer`: the target sequence to be counted  
- Sample Call  
`http://test.test/recoverString?args=[426689]`  
Queries the string at index `426689` in the dataset held by `test.test`

### findIndicesOfStr

Queries the index if the given string.

- Arguments  
    `seq::String`: the target sequence to be counted  
    `givenRange::(Long, Long)`: (OPTIONAL) Restricts the query to the given range  
- Sample Call  
`http://test.test/findIndicesOfStr?args=["CATAGAT"]`  
Queries the dataset for the index for the string `CATAGAT` in the dataset held by `test.test`

### getSequenceDollarID

Queries the BWT end marker index for the given sequence

- Arguments  
    `seq::String`: the target sequence to be counted  
    `returnOffset::Boolean`: (OPTIONAL - defaults to false) True will query the offset
- Sample Call  
`http://test.test/getSequenceDollarID?args=["CATAGAT"]`  
Queries the dataset for the index for the string `CATAGAT` in the dataset held by `test.test`

### Optional Arguments

Optional arguments may be specified as an additional url parameter in the form:  
`&argument_name=argument_value`  
after the `args` parameter

#### Example

`http://test.test/getSequenceDollarID?args=["CATAGAT"]&returnOffset=True` 

### Batch Queries

The following batch functions queue several queries of the same type under a single token

#### batchRecoverString

Queries all strings in the given range of indices

- Arguments  
    `startIndex:Long`: the start of the range of indices to be queried  
    `endIndex:Long`: the end of the range of indices to be queried  
    `returnOffset::Boolean`: (OPTIONAL - defaults to false) True will query the offset
- Sample Call  
`http://test.test/batchRecoverString?args=[1346091641L, 15700916349L]`

#### batchCountOccurrencesOfSeq

Queries counts of a list of sequences

- Arguments  
    `seqList::List<String>`: List of sequences to be counted  
    `givenRange::(Long, Long)`: (OPTIONAL) Restricts the query to the given range
- Sample Call  
`http://test.test/batchCountOccurrencesOfSeq?args=["CATAGAT", "GATTACA"]`

#### batchFastCountOccurrences

Optimized Routine to count occurrences of a list of sequences

- Arguments  
    `seqList::List<String>`: List of sequences to be counted  
- Sample Call  
`http://test.test/batchFastCountOccurrences?args=['CATAGAT', 'GATTACA']`

### Return Structure

The functions above do not directly return their results to prevent blocking on long running calls. Instead, a token is given that can be used to retrieve the status of a query.  

#### Sample Return JSON for countOccurrencesOfSeq

```json
{
    "function": "countOccurrencesOfSeq",
    "token"   : "SqFg2Pjrko8qhFz",
    "args"    : ["CATAGAT"],
    "kwargs"  : {},
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male",
                "load"        : 4
    }
}
```

### Obtaining Results

The status of a query can be obtained using the token value returned by the above functions. The token is passed to the url:  

`/results/<token>`

#### Status Codes

`200`: Successfully retrieved token status  
`404`: Token not found  

#### Sample Results JSON for Running Query

``` json
{
    "date"    : "01/01/1990, 00:00:00",
    "function" : "countOccurrencesOfSeq",
    "args"    : ["CATAGAT"],
    "kwargs"  : {},
    "status"  : "RUNNING",
    "result"  : null,
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male",
                "load"        : 4
    }
}
```

#### Sample Results JSON for Successful Quey

```json
{
    "date"    : "01/01/1990, 00:00:00",
    "function" : "countOccurrencesOfSeq",
    "args"    : ["CATAGAT"],
    "kwargs"  : {},
    "status"  : "SUCCESS",
    "result"  : 9327856,
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male",
                "load"        : 4
    }
}
```

#### Sample Results JSON for Failed Quey

``` json
{
    "date"    : "01/01/1990, 00:00:00",
    "function" : "countOccurrencesOfSeq",
    "args"    : ["CATAGAT", "TAGA", "GATACCA"],
    "kwargs"  : {},
    "status"  : "FAILED",
    "result"  : "ValueError: countOccurrencesOfSeq takes exactly one argument",
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male",
                "load"        : 4
    }
}
```