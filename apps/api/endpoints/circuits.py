from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.models import a_circuit
from api.logic import data_store

ns = api.namespace('circuits', description='Define a circuit around which a race laps')

@ns.route('/')
class Circuits(Resource):
	@api.response(200, 'Circuits found')
	def get(self):
		return data_store.get_circuits()

	@api.expect(a_circuit)
	@api.response(201, 'Circuit created')
	def post(self):
		doc = data_store.create_circuit(api.payload)
		return doc, 201

@ns.route('/<int:id>')
@api.response(404, 'Circuit not found')
class Circuit(Resource):
	def get(self, id):
		"""Returns details of a circuit"""
		circuit = data_store.get_circuit(id)
		if circuit:
			return circuit, 200
		else:
			return None, 404

	@api.expect(a_circuit)
	@api.response(204, 'Circuit updated')
	def put(self, id):
		"""Updates attributes of an existing circuit"""
		if data_store.get_circuit(id):
			data_store.update_circuit(id, api.payload)
			return None, 204
		else:
			return None, 404

	@api.response(204, 'Circuit deleted')
	def delete(self, id):
		"""Deletes an existing circuit"""
		if data_store.get_circuit(id):
			data_store.delete_circuit(id)
			return None, 204
		else:
			return None, 404
