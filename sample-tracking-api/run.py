import yaml
from app.app import app
import os
config = os.path.join(os.path.dirname(os.path.realpath(__file__)) , "app/lims_user_config")
config_options = yaml.safe_load(open(config , "r"))
DEBUG=False
ENV = config_options['env']
if ENV == 'local' or ENV == 'dev':
    DEBUG = True
elif ENV == 'prod':
    DEBUG = False
# dev, this is how python runs the app
if __name__ == '__main__':
    app.run(debug=DEBUG, threaded=True)