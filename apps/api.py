from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json

app = Flask(__name__, static_url_path='')

db_name = 'events'
client = None
db = None

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

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('index.html')

# /**
#  * Endpoint to get a JSON array of all the events in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/events
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the event titles
#  */
@app.route('/api/events', methods=['GET'])
def get_events():
    if client:
        return jsonify(list(map(lambda doc: doc['title'], db)))
    else:
        print('No database connection')
        return jsonify([])


# /* Endpoint to greet and add a new visitor to database.
# * See https://github.com/rosscado/raceready/wiki/Data-Model#event
# * Send a POST request to localhost:8000/api/events with body
# * {
# *     "title": "Bob"
# * }
# */
@app.route('/api/events', methods=['POST'])
def put_event():
    title = request.json['title']
    data = {'title':title}
    if client:
        event_doc = db.create_document(data)
        data['_id'] = event_doc['_id']
        return jsonify(data)
    else:
        print('No database connection')
        return jsonify(data)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
