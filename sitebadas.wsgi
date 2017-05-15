python_home = '/hosting/users/wilson.jallet/venv'

activate_this = python_home + '/bin/activate'
execfile(activate_this, dict(__file__=activate_this))
from sitebadas import app as application
