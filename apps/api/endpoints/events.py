from flask import request
from flask_restplus import Resource, fields
from api.restplus import api

ns = api.namespace('events', description='Operations related to scheduled events')
an_event = api.model('Event', {'title' : fields.String('The name of the event as promoted publically')})

events = []
beggs = {'title': 'John Beggs Memorial'}
events.append(beggs)

@ns.route('/')
class Event(Resource):
	def get(self):
		return events

	@api.expect(an_event)
	def post(self):
		events.append(api.payload)
		return api.payload, 201
