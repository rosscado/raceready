import pytest
from resource import ResourceTestCase

@pytest.fixture
def resource_name():
	return 'categories'

@pytest.fixture
def resource_data():
	return {
		'id': 'A1',
		'description': 'The highest amateur open road racing league in Ireland'
	}

@pytest.fixture
def required_fields():
	return ['id']


class TestCategories(ResourceTestCase):
	# must declare ns fixture in this module to override dependent fixtures
	ns = '/api/{resources}/'.format(resources=resource_name())

	def test_posted_category_has_id(self, client, resource_fixture):
		"""Test that POST responses contain id"""
		assert 'id' in resource_fixture
