import os

DEFAULT_API_KEY = "d186b10e-694d-4ede-9689-55f36514b058"

#Who knows if this is okay right now... bah
REFRESH_INTERVAL = 100  # Milliseconds
TOTAL_COLUMNS = 4

# This doesn't exist, but the Default does exist
RTD_API_KEY = os.environ.get('RTD_API_KEY')

### This csv with stations doesn't exist... and the default doesn't exist
HOME_LIST = 'home.csv'
WORK_LIST = 'work.csv'