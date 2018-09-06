from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.logic import one_day_event as an_event, data_store

ns = api.namespace('events', description='Operations related to scheduled events')

@ns.route('/')
class Events(Resource):
	@api.response(200, 'Events found')
	def get(self):
		return data_store.get_events()

	@api.expect(an_event)
	@api.response(201, 'Event created')
	def post(self):
		doc = data_store.create_event(api.payload)
		return doc, 201

@ns.route('/<int:id>')
@api.response(404, 'Event not found')
class Event(Resource):
	def get(self, id):
		"""Returns details of an event"""
		event = data_store.get_event(id)
		if event:
			return event, 200
		else:
			return None, 404

	@api.expect(an_event)
	@api.response(204, 'Event updated')
	def put(self, id):
		"""Updates attributes of an existing event"""
		if data_store.get_event(id):
			data_store.update_event(id, api.payload)
			return None, 204
		else:
			return None, 404

	@api.response(204, 'Event deleted')
	def delete(self, id):
		"""Deletes an existing event"""
		if data_store.get_event(id):
			data_store.delete_event(id)
			return None, 204
		else:
			return None, 404
