'''This module encapsulates database functions
and can be used to obtain a database client for
any of the application's databases'''
import os
import json
from cloudant import Cloudant
from flask import g, app

def init_db(config):
	if not 'DATABASE' in config:
		print("Error: I don't know which database to use!")
	get_db(config['DATABASE'])

def get_db(db_name='events'):
	'''Return a CloudantDatabase object'''
	if 'db_client' not in g:
		g.db_client = connect_db(db_name)
	if db_name not in g.db_client:
		g.db_client = connect_db(db_name, client=client)
	return g.db_client[db_name]

def shutdown_db():
	db_client = g.pop('db_client', None)
	if db_client is not None:
		db_client.disconnect()

def connect_db(db_name, db_client=None):
	'''Connect a database client to the server configured in VCAP_SERVICES
	and open the named database.
	If the database does not exist it will be created.
	Returns the database client.'''
	db = None
	client = db_client
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
	elif os.path.isfile('apps/vcap-local.json'):
		with open('apps/vcap-local.json') as f:
			vcap = json.load(f)
			print('Found local VCAP_SERVICES')
			creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
			user = creds['username']
			password = creds['password']
			url = 'https://' + creds['host']
			client = Cloudant(user, password, url=url, connect=True)
			db = client.create_database(db_name, throw_on_exists=False)
	else:
		print('No VCAP_SERVICES found')
	if db is not None:
		print('Connected to {0} database'.format(db_name))
	return client
