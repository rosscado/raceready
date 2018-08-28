from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.logic import a_club, data_store

ns = api.namespace('clubs', description='Operations related to cycling clubs')

@ns.route('/')
class Clubs(Resource):
	@api.response(200, 'Clubs found')
	def get(self):
		return data_store.get_clubs()

	@api.expect(a_club)
	@api.response(201, 'Club created')
	def post(self):
		doc = data_store.create_club(api.payload)
		return doc, 201

@ns.route('/<int:id>')
@api.response(404, 'Club not found')
class Club(Resource):
	def get(self, id):
		"""Returns details of an club"""
		club = data_store.get_club(id)
		if club:
			return club, 200
		else:
			return None, 404

	@api.expect(a_club)
	@api.response(204, 'Club updated')
	def put(self, id):
		"""Updates attributes of an existing club"""
		if data_store.get_club(id):
			data_store.update_club(id, api.payload)
			return None, 204
		else:
			return None, 404

	@api.response(204, 'Club deleted')
	def delete(self, id):
		"""Deletes an existing club"""
		if data_store.get_club(id):
			data_store.delete_club(id)
			return None, 204
		else:
			return None, 404
