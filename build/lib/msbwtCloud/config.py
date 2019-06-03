# Configuration values for msbwtCloud
# Values can be accessed at app.config['KEY']

#### General Info ####

# General service information
DATA = {
    'name': "CC027M756_UNC_NYGC",
    'description': "Collaborative Cross Dataset 27 Male",
}

#### BWT ####

# Location of the BWT (Full path with trailing '/')
BWT_ROOT = '/home/a2/msbwtStorage/CC027M756_UNC_NYGC/'.encode('utf-8', 'ignore')

##### DATABASE ####

# Location of Database file
DB_ROOT = '/home/a2/msbwtCloud/msbwtCloud/msbwt.sqlite'

# Duration that queries remain in database (days)
DB_QUERY_LIFE = 1.0
