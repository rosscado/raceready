from flask import request
from flask_restplus import Resource
from apps.api.restplus import api

ns = api.namespace('events', description='Operations related to scheduled events')

events = {}

@ns.route('/<string:id>')
class Event(Resource):
	def get(self, id):
		return {'title': events[id]['title']}

	def put(self, id):
		events[id] = {'title': request.form['title']}
		return {'title': request.form['title']}
