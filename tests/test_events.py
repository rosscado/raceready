import pytest
from resource import ResourceTestCase
from context import app # check sys.path if this fails

arbitrary_title='Unit test event' # default event fixture title
arbitrary_date='1970-01-01' # a date to use when the date doesn't matter (UNIX epoch)
arbitrary_type='road race' # default event fixture type

@pytest.fixture
def resource_fixture(client):
	'''POST an event for use in test cases and return its JSON object
	Assumes that the `test_post_events` testcase passes'''
	event_input = {'title': arbitrary_title, 'date': arbitrary_date, 'type': arbitrary_type}
	post_rv = client.post('/api/events/', json=event_input)
	event_result = post_rv.get_json()
	yield event_result

	client.delete('/api/events/{id}'.format(id=event_result['id']))

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

	def test_post_events(self, client):
		'''Test POST /events API for event creation'''
		resource_fixture = {
			'title': 'The John Beggs',
			'date': '2018-08-11',
			'url': 'https://goo.gl/tVymnx',
			'location': 'Dromore, Co. Down',
			'type': 'road race'
		}

		self._test_post_resource(client, resource_fixture)

	def test_post_events_required_fields(self, client):
		'''Test POST /events API for event creation when missing required fields'''
		resource_fixture = {'title': arbitrary_title, 'date': arbitrary_date, 'type': arbitrary_type}

		self._test_post_resource_required_fields(client, resource_fixture)

	def test_post_events_invalid_date(self, client):
		'''Test POST /events API for event creation when date field is not ISO format'''
		resource_fixture = {'title': arbitrary_title, 'date': arbitrary_date, 'type': arbitrary_type}

		self._test_post_resource_invalid_field(client, resource_fixture, {'date': 'foo bar'})
		self._test_post_resource_invalid_field(client, resource_fixture, {'date': '2018/08/11'})
		self._test_post_resource_invalid_field(client, resource_fixture, {'date': '11-08-2018'})

	def test_post_events_invalid_type(self, client):
		'''Test POST /events API for event creation when type field is note a recognised value'''
		resource_fixture = {'title': arbitrary_title, 'date': arbitrary_date, 'type': arbitrary_type}

		self._test_post_resource_invalid_field(client, resource_fixture, {'type': 'foo bar'})
		self._test_post_resource_invalid_field(client, resource_fixture, {'type': 'race'})

	def test_put_event_not_found(self, client):
		"""Test PUT /events/{id} API with a non-existent {id}"""
		no_such_resource_fixture = {'title': arbitrary_title, 'date': arbitrary_date, 'type': arbitrary_type}
		self._test_put_resource_not_found(client, no_such_resource_fixture)

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
