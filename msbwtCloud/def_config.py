# Configuration values for msbwtCloud
# Values can be accessed at app.config['KEY']

#### General Info ####

# General service information

DATA = {
    'name': "Name of Dataset or Preference",
    'description': "Description of dataset",
}

#### BWT ####

# Location of the BWT (Full path with trailing '/')
BWT_ROOT = '/path/to/bwt/folder'.encode('utf-8', 'ignore')

##### DATABASE ####

# Location of Database file
DB_ROOT = '/path/to/database/file.sqlite'

# Duration that queries remain in database (days)
DB_QUERY_LIFE = 1.0
