# Configuration values for msbwtCloud
# Values can be accessed at app.config['KEY']

#### General Info ####

# General service information
LEGACY = True
print("modified")

DATA = {
    'name': "UNC csbio msBWT server",
    'description': "Collaborative Cross Dataset 27 Male",
}

#### BWT ####

# Location of the BWT (Full path with trailing '/')
BWT_ROOT = '/playpen/msbwtCloud/msbwtStorage/'.encode('utf-8', 'ignore')

##### DATABASE ####

# Location of Database file
DB_ROOT = '/playpen/msbwtCloud/msbwtCloud/msbwt.sqlite'

# Duration that queries remain in database (days)
DB_QUERY_LIFE = 1.0

# Number of query workers (concurrent query operations)
# More than one may result in memory conflicts resulting in lower performance
QUERY_WORKERS = 1
