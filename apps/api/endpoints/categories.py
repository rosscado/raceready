from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.models import a_category
from api.logic import data_store

ns = api.namespace('categories', description='Define a competitor category')

@ns.route('/')
class Categories(Resource):
	@api.response(200, 'Categories found')
	def get(self):
		return data_store.get_categories()

	@api.expect(a_category)
	@api.response(201, 'Category created')
	def post(self):
		doc = data_store.create_category(api.payload)
		return doc, 201

@ns.route('/<string:id>')
@api.response(404, 'Category not found')
class Category(Resource):
	def get(self, id):
		"""Returns details of a category"""
		category = data_store.get_category(id)
		if category:
			return category, 200
		else:
			return None, 404

	@api.expect(a_category)
	@api.response(204, 'Category updated')
	def put(self, id):
		"""Updates attributes of an existing category"""
		if data_store.get_category(id):
			data_store.update_category(id, api.payload)
			return None, 204
		else:
			return None, 404

	@api.response(204, 'Category deleted')
	def delete(self, id):
		"""Deletes an existing category"""
		if data_store.get_category(id):
			data_store.delete_category(id)
			return None, 204
		else:
			return None, 404
