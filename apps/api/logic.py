from flask_restplus import fields
from api.restplus import api

from database.clients import get_db
from cloudant.result import Result

# this module contains business logic for CRUD of resources
# it determines how and where to persist server-side resources

an_event = api.model('Event', {
	'id': fields.Integer(description='The unique identifier of an event (internal)', readonly=True),
	'title': fields.String(required=True, description='The name of the event as promoted publically', example='The John Beggs Memorial'),
	'date': fields.Date(required=True,description='When will the event take place? ISO 8601 format: YYYY-MM-DD', example='2018-08-11'),
	'url': fields.String(description='The primary URL promoting the event', example='http://www.banbridgecc.com/thebeggs18/'),
	'location': fields.String(description='The address of the event. Should identify at least the town.', example='Donore, Co. Down'),
	'type': fields.String(required=True,description='The type of event. Is a road race, time trial, etc?', enum=['road race', 'time trial', 'hill climb', 'criterium', 'stage race'], default='road race', example='road race')
	})

events = []

def get_events():
	#db = get_db('events')
	#print("listing documents in events database".format(db.all_docs()))
	#all_events = Result(db.all_docs, include_docs=True)
	#return [event for event in all_events]
	return events

def create_event(payload):
	#doc = db_client.create_document(api.payload)
	events.append(payload)
	doc = payload
	doc['id'] = len(events)
	return doc

def get_event(id):
	if 0 < id <= len(events):
		return events[id-1]
	else:
		return None

def update_event(id, payload):
	events[id-1] = payload

def delete_event(id):
	del events[id-1]
