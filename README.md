# msBWT Server and Cloud


## msBWT RESTful interface and Name Resolution

A paired server combination implemented with Flask. msbwtCloud provides an RESTful interface for non-blocking requests to a remote msBWT data structure. Queries return a token and summary and results can be retrieved by providing the token. msbwtServer provides name resolution and management for multiple remote msBWT structures including status checking, dynamic response to resource movement, and a basic web interface.

## Installation 
- Clone this repository on to the device hosting the BWT datastructure.
- TODO

## msBWTCloud

msBWTCloud provides the primary interface for interacting with remote BWT data structures. The following functions are exposed at:
```
    /<function_name>?args=[args_list]
```

### countOccurrencesOfSeq
Queries the number of times a sequence occurrs in the target dataset.

- Arguments  
    `'seq'`: the target sequence to be counted
- Sample Call  
`http://test.test/countOccurrencesOfSeq?args=['CATAGAT']`  
Queries the number of occurrences of `CATAGAT` in the dataset held by `test.test`
 
### Return Structure
The functions above do not directly return their results to prevent blocking on long running calls. Instead, a token is given that can be used to retrieve the status of a query.  
#### Sample Return JSON for countOccurrencesOfSeq
```
{
    "function": "countOccurrencesOfSeq",
    "token"   : "SqFg2Pjrko8qhFz",
    "args"    : ['CATAGAT'],
    "kwargs"  : {},
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male"
                "load"        : 4
    }
}
```

## Obtaining Results
The status of a query can be obtained using the token value returned by the above functions. The token is passed to the url:  
```
/results/<token>
```
#### Sample Results JSON for Running Query
```
{
    "date"    : "01/01/1990, 00:00:00",
    "function : "countOccurrencesOfSeq",
    "args"    : ['CATAGAT']
    "kwargs"  : {}
    "status"  : "RUNNING"
    "result"  : null,
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male"
                "load"        : 4
    }
}
```
#### Sample Results JSON for Successful Quey
```
{
    "date"    : "01/01/1990, 00:00:00",
    "function : "countOccurrencesOfSeq",
    "args"    : ['CATAGAT']
    "kwargs"  : {}
    "status"  : "SUCCESS"
    "result"  : 9327856,
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male"
                "load"        : 4
    }
}
```

#### Sample Results JSON for Successful Quey
```
{
    "date"    : "01/01/1990, 00:00:00",
    "function : "countOccurrencesOfSeq",
    "args"    : ['CATAGAT']
    "kwargs"  : {}
    "status"  : "FAILED"
    "result"  : "ValueError: countOccurrencesOfSeq takes exactly one argument",
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male"
                "load"        : 4
    }
}
```





