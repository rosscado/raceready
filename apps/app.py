from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, Blueprint
from flask_restplus import Resource, Api
from apps.api.restplus import api
from apps.api.endpoints.events import ns as events_namespace
import atexit
import os
import json

def init_db():
    db_name = 'events'
    db = None
    client = None
    if 'VCAP_SERVICES' in os.environ:
        vcap = json.loads(os.getenv('VCAP_SERVICES'))
        print('Found VCAP_SERVICES')
        if 'cloudantNoSQLDB' in vcap:
            creds = vcap['cloudantNoSQLDB'][0]['credentials']
            user = creds['username']
            password = creds['password']
            url = 'https://' + creds['host']
            client = Cloudant(user, password, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)
    elif os.path.isfile('vcap-local.json'):
        with open('vcap-local.json') as f:
            vcap = json.load(f)
            print('Found local VCAP_SERVICES')
            creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
            user = creds['username']
            password = creds['password']
            url = 'https://' + creds['host']
            client = Cloudant(user, password, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)
    return client

def init_app(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(events_namespace)
    flask_app.register_blueprint(blueprint)

@atexit.register
def shutdown():
    if client:
        client.disconnect()


app = Flask(__name__, static_url_path='')
client = init_db()
init_app(app)
# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
