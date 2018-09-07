from flask import Flask, render_template, request, jsonify, Blueprint
from flask_restplus import Resource, Api
from database.clients import init_db, shutdown_db
from api.restplus import api
from api.endpoints.events import ns as events_namespace
from api.endpoints.clubs import ns as clubs_namespace
from api.endpoints.circuits import ns as circuits_namespace
from api.endpoints.categories import ns as categories_namespace
import atexit
import os
import json

def init_app(flask_app):
	app.config['DATABASE'] = 'events'

	blueprint = Blueprint('api', __name__, url_prefix='/api')
	api.init_app(blueprint)
	api.add_namespace(events_namespace)
	api.add_namespace(clubs_namespace)
	api.add_namespace(circuits_namespace)
	api.add_namespace(categories_namespace)
	flask_app.register_blueprint(blueprint)

@atexit.register
def shutdown():
	with app.app_context():
		shutdown_db()

app = Flask(__name__, static_url_path='')
init_app(app)
with app.app_context():
	init_db(app.config)
# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)
