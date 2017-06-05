from agro_db.settings.pool import init_pool
from django.db import close_old_connections
import os
from os.path import dirname, abspath, exists
import django
from flask import Flask
from flask.ext.cors import CORS
from lastmiledelivery.utils.uniform_caching_interface import init_cache_handlers
from lastmiledelivery.utils.get_lead_auth_token import get_leadgen_authtoken
from flask.ext.gzip import Gzip

# initialize DB connections
close_old_connections()
init_pool()
django.setup()

app = Flask(__name__)
gzip = Gzip(app)
app.root_dir = dirname(dirname(abspath(__file__)))
CORS(app)

# setup logger
from lastmiledelivery.conf.logger_setup import setup_config_logger

setup_config_logger(app)

# initialize cache handler
app.global_cache_handler = init_cache_handlers(app)
app.logger.info(app.global_cache_handler)

# initializing the user service interface for auth
from lastmiledelivery.conf.session_interfaces import UserServiceInterface

app.session_interface = UserServiceInterface()
app.leadgen_auth_token = get_leadgen_authtoken("AgroExService","agroexpass")

# wrap app into flask restful extention
from flask.ext import restful

api = restful.Api(app, prefix='/api/v3/')

# set config
from lastmiledelivery.conf.config_setup import set_config

set_config(app)

# initialize boot-time variables
from lastmiledelivery.conf.init_startup_variables import init_variables

init_variables(app)

# initialize url mapping
from lastmiledelivery.conf.router import setup_routing

setup_routing(api)

if __name__ == "__main__":
	app.run(host="127.0.0.1",debug=True,port=9842, processes=4)

