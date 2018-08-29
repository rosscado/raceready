import pytest
from resource import ResourceTestCase
from context import app # check sys.path if this fails

arbitrary_title='Unit test event' # default event fixture title
arbitrary_date='1970-01-01' # a date to use when the date doesn't matter (UNIX epoch)
arbitrary_type='road race' # default event fixture type


@pytest.fixture
def resource_name():
	return 'events'

@pytest.fixture
def resource_data():
	return {
		'title': 'The John Beggs',
		'date': '2018-08-11',
		'url': 'https://goo.gl/tVymnx',
		'location': 'Dromore, Co. Down',
		'type': 'road race'
	}

# test case functions
def test_swagger(client):
	"""Test application root hosts swagger docs"""
	rv = client.get('/api/')
	assert b'swagger' in rv.data


class TestEvents(ResourceTestCase):

	# namespace must be declared as a class variable
	# rather than an instance variable because pytest classes
	# can't have __init__ functions
	# https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery
	ns = '/api/events/'

	def test_post_events_required_fields(self, client):
		'''Test POST /events API for event creation when missing required fields'''
		resource_fixture = {'title': arbitrary_title, 'date': arbitrary_date, 'type': arbitrary_type}

		self._test_post_resource_required_fields(client, resource_fixture)

	def test_post_events_invalid_date(self, client, resource_data):
		'''Test POST /events API for event creation when date field is not ISO format'''
		self._test_post_resource_invalid_field(client, resource_data, {'date': 'foo bar'})
		self._test_post_resource_invalid_field(client, resource_data, {'date': '2018/08/11'})
		self._test_post_resource_invalid_field(client, resource_data, {'date': '11-08-2018'})

	def test_post_events_invalid_type(self, client, resource_data):
		'''Test POST /events API for event creation when type field is note a recognised value'''
		self._test_post_resource_invalid_field(client, resource_data, {'type': 'foo bar'})
		self._test_post_resource_invalid_field(client, resource_data, {'type': 'race'})

	def test_put_event_required_fields(self, client, resource_fixture):
		"""Test PUT /events/{id} API for event modification when required fields are missing"""
		resource_fixture_min = {
			'title': resource_fixture['title'],
			'date': resource_fixture['date'],
			'type': resource_fixture['type']
			}
		self._test_put_resource_required_fields(client, resource_fixture['id'], resource_fixture_min)

	def test_put_event_status(self, client, resource_fixture):
		"""Test PUT /events/{id} API for event status modification"""
		assert 'status' not in resource_fixture # test has default status
		event_status = {'state': 'cancelled', 'url': 'http://sorryaboutthat.com/notice'}
		self._test_put_resource_field(client, resource_fixture, ('status', event_status))
