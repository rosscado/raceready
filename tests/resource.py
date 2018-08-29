import pytest

# test assertion functions
def assert_list(obj):
	'''Return True iff obj is a list-like object'''
	assert 'index' in dir(obj) and 'append' in dir(obj)


class ResourceTestCase:
	non_existent_resource_id='007404007' # does not match an resource, reliably gives a 404

	def get_resource_fixture(self, client, id):
		'''Return a resource for use in test cases
		Assumes that the `test_get_resource` testcase passes
		and that a resource with {id} has already been created.
		Returns None (does not raise an error) if resource not found'''
		get_rv = client.get('{ns}{id}'.format(ns=self.ns,id=id))
		if get_rv.status_code == 404:
			return None
		else:
			return get_rv.get_json()

	def test_get_resources(self, client):
		"""Test GET /namespace API for resource listing"""
		get_rv = client.get(self.ns)
		assert get_rv.status_code == 200
		resources_result = get_rv.get_json()
		assert resources_result is not None
		assert_list(resources_result)

	def test_get_resources_not_empty(self, client, resource_fixture):
		"""Test GET /namespace API for resource listing when resources do exist"""
		get_rv = client.get(self.ns)
		resources_result = get_rv.get_json()
		assert resources_result # assert that list is not None or empty

	def test_post_resource(self, client, resource_data):
		post_rv = client.post(self.ns, json=resource_data)
		assert post_rv.status_code == 201
		resource_result = post_rv.get_json()
		assert resource_result is not None
		for field in resource_data:
			assert resource_result[field] == resource_data[field]

	def test_post_resource_required_fields(self, client, resource_data, required_fields):
		'''Given a resource fixture input payload
		test that the API will reject requests to create the resource
		if any of those fields are missing'''
		for field in required_fields:
			del resource_data[field]
			post_rv = client.post(self.ns, json=resource_data)
			assert post_rv.status_code == 400

	def _test_post_resource_invalid_field(self, client, resource_fixture, invalid_field):
		'''Given a valid resource fixture
		test that the API will reject requests to create the resource
		if a specified field is invalidated'''
		(fieldname, value) = list(invalid_field.items())[0]
		resource_fixture[fieldname] = value
		post_rv = client.post(self.ns, json=resource_fixture)
		assert post_rv.status_code == 400

	def test_get_resource(self, client, resource_fixture):
		"""Test GET /{resource}/{id} API"""
		get_rv = client.get('{namespace}{id}'.format(namespace=self.ns, id=resource_fixture['id']))
		assert get_rv.status_code == 200
		resource_result = get_rv.get_json()
		assert resource_result is not None
		for property in resource_fixture:
			assert resource_result[property] == resource_fixture[property]

	def test_get_resource_not_found(self, client):
		"""Test GET /{resource}/{id} API with a non-existent {id}"""
		get_rv = client.get('{namespace}{id}'.format(namespace=self.ns, id=self.non_existent_resource_id))
		assert get_rv.status_code == 404

	def test_put_resource(self, client, resource_fixture):
		put_rv = client.put('{namespace}{id}'.format(namespace=self.ns, id=resource_fixture['id']), json=resource_fixture)
		assert put_rv.status_code == 204
		resource_result = self.get_resource_fixture(client, resource_fixture['id'])
		for property in resource_fixture:
			assert resource_result[property] == resource_fixture[property]

	def test_put_resource_not_found(self, client, resource_fixture):
		put_rv = client.put('{ns}{id}'.format(ns=self.ns,id=self.non_existent_resource_id), json=resource_fixture)
		assert put_rv.status_code == 404

	def test_put_resource_required_fields(self, client, resource_fixture, required_fields):
		'''Given an existing resource fixture
		test that the API will reject requests to update the resource
		if any of those fields are missing'''
		for field in required_fields:
			del resource_fixture[field]
			post_rv = client.put('{ns}{id}'.format(ns=self.ns, id=resource_fixture['id']), json=resource_fixture)
			assert post_rv.status_code == 400

	def test_delete_resource(self, client, resource_fixture):
		delete_rv = client.delete('{ns}{id}'.format(ns=self.ns,id=resource_fixture['id']))
		assert delete_rv.status_code == 204
		resource_result = self.get_resource_fixture(client, resource_fixture['id'])
		assert resource_result is None

	def test_delete_resource_not_found(self, client):
		"""Test DELETE /{resource}/{id} API with a non-existent {id}"""
		delete_rv = client.delete('{ns}{id}'.format(ns=self.ns,id=self.non_existent_resource_id))
		assert delete_rv.status_code == 404

	def _test_put_resource_field(self, client, resource_fixture, field):
		# this test case seems a lot like _test_put_resource, is it necessary?
		(name, value) = field
		resource_fixture[name] = value
		put_rv = client.put('{ns}{id}'.format(ns=self.ns,id=resource_fixture['id']), json=resource_fixture)
		assert put_rv.status_code == 204
		resource_result = self.get_resource_fixture(client, resource_fixture['id'])
		assert name in resource_result and resource_result[name] == resource_fixture[name]
