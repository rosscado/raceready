'''
This module contains business logic for CRUD of resources
It determines how and where to persist server-side resources
'''

from flask_restplus import fields
from api.restplus import api

class TransientModel:
	def __init__(self):
		self.events = []

	def get_events(self):
		return self.events

	def create_event(self, payload):
		#doc = db_client.create_document(api.payload)
		self.events.append(payload)
		doc = payload
		doc['id'] = len(self.events)
		return doc

	def get_event(self, id):
		if 0 < id <= len(self.events):
			return self.events[id-1]
		else:
			return None

	def update_event(self, id, payload):
		self.events[id-1] = payload

	def delete_event(self, id):
		del self.events[id-1]


from database.clients import get_db
from cloudant.result import Result
class PeristentModel:
	def __init__(self, db_name):
		self.db = get_db(db_name)

	def get_events(self):
		print("listing documents in events database".format(db.all_docs()))
		all_events = Result(db.all_docs, include_docs=True)
		return [event for event in all_events]

event_status = api.model('Status', {
	'state': fields.String(description='Is the event still on?', enum=['scheduled', 'provisional', 'cancelled', 'completed'], default='scheduled', example='scheduled'),
	'url': fields.String(description='The primary URL where notice of the most recent state change was posted', example='http://www.banbridgecc.com/eventcancellation/')
})

an_event = api.model('Event', {
	'id': fields.Integer(description='The unique identifier of an event (internal)', readonly=True),
	'title': fields.String(required=True, description='The name of the event as promoted publically', example='The John Beggs Memorial'),
	'date': fields.Date(required=True,description='When will the event take place? ISO 8601 format: YYYY-MM-DD', example='2018-08-11'),
	'url': fields.String(description='The primary URL promoting the event', example='http://www.banbridgecc.com/thebeggs18/'),
	'location': fields.String(description='The address of the event. Should identify at least the town.', example='Donore, Co. Down'),
	'type': fields.String(required=True,description='The type of event. Is a road race, time trial, etc?', enum=['road race', 'time trial', 'hill climb', 'criterium', 'stage race'], default='road race', example='road race'),
	'status': fields.Nested(event_status, description='Records any schedule changes. If absent assume event is still scheduled normally')
	})

data_store = TransientModel()
