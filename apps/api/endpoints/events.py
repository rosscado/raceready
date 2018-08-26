from flask import request
from flask_restplus import Resource, fields
from api.restplus import api
from database.clients import get_db
from cloudant.result import Result

ns = api.namespace('events', description='Operations related to scheduled events')
an_event = api.model('Event', {
	'id': fields.Integer(description='The unique identifier of an event (internal)', readonly=True),
	'title': fields.String(required=True, description='The name of the event as promoted publically', example='The John Beggs Memorial'),
	'date': fields.Date(required=True,description='When will the event take place? ISO 8601 format: YYYY-MM-DD', example='2018-08-11'),
	'url': fields.String(description='The primary URL promoting the event', example='http://www.banbridgecc.com/thebeggs18/'),
	'location': fields.String(description='The address of the event. Should identify at least the town.', example='Donore, Co. Down'),
	'type': fields.String(required=True,description='The type of event. Is a road race, time trial, etc?', enum=['road race', 'time trial', 'hill climb', 'criterium', 'stage race'], default='road race', example='road race')
	})

events = []

@ns.route('/')
class Events(Resource):
	@api.response(200, 'Events found')
	def get(self):
		#db = get_db('events')
		#print("listing documents in events database".format(db.all_docs()))
		#all_events = Result(db.all_docs, include_docs=True)
		#return [event for event in all_events]
		return events

	@api.expect(an_event)
	@api.response(201, 'Event created')
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
		if 0 < id <= len(events):
			return events[id-1], 200
		else:
			return None, 404

	@api.expect(an_event)
	@api.response(204, 'Event updated')
	def put(self, id):
		"""Updates attributes of an existing event"""
		if 0 < id <= len(events):
			events[id-1] = api.payload
			return None, 204
		else:
			return None, 404

	@api.response(204, 'Event deleted')
	def delete(self, id):
		"""Deletes an existing event"""
		if 0 < id <= len(events):
			del events[id-1]
			return None, 204
		else:
			return None, 404
