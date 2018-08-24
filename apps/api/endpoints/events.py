from flask import request
from flask_restplus import Resource, fields
from api.restplus import api
from database.clients import get_db
from cloudant.result import Result

ns = api.namespace('events', description='Operations related to scheduled events')
an_event = api.model('Event', {'title' : fields.String('The name of the event as promoted publically')})

events = []

@ns.route('/')
class Events(Resource):
	def get(self):
		db = get_db('events')
		print("listing documents in events database".format(db.all_docs()))
		all_events = Result(db.all_docs, include_docs=True)
		return [event for event in all_events]
		#return events

	@api.expect(an_event)
	def post(self):
		#doc = db_client.create_document(api.payload)
		events.append(api.payload)
		doc = api.payload
		doc['id'] = len(events)
		return doc, 201

@ns.route('/<int:id>')
@api.response(404, 'Event not found')
class Event(Resource):
	def get(self, id):
		"""Returns details of an event"""
		return events[id-1]
