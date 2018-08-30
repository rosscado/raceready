import pytest
from resource import ResourceTestCase
from context import app # check sys.path if this fails

arbitrary_title='Unit test event' # default event fixture title
arbitrary_date='1970-01-01' # a date to use when the date doesn't matter (UNIX epoch)
arbitrary_event_type='road race' # default event fixture type


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
		'event_type': 'road race'
	}

@pytest.fixture
def required_fields():
	return ['title', 'date', 'event_type']

@pytest.fixture
def signon_data():
	return {
		'venue': 'GAA club, Dromore, Co. Down',
		'start_time': '2018-08-11 09:30',
		'end_time': '2018-08-11 11:30'
	}

@pytest.fixture
def category_data():
	return {'id': 'A1'}

@pytest.fixture
def stage_data(category_data):
	return {
		'distance_km': 96,
		'start_time': '2018-08-11 12:00',
		'stage_type': 'road race',
		'eligible_categories': [category_data['id']],
		'title': 'headline race'
	}

# test case functions
def test_swagger(client):
	"""Test application root hosts swagger docs"""
	rv = client.get('/api/')
	assert b'swagger' in rv.data


class TestEvents(ResourceTestCase):
	ns = '/api/{resources}/'.format(resources=resource_name())

	def test_post_events_invalid_date(self, client, resource_data):
		'''Test POST /events API for event creation when date field is not ISO format'''
		self._test_post_resource_invalid_field(client, resource_data, {'date': 'foo bar'})
		self._test_post_resource_invalid_field(client, resource_data, {'date': '2018/08/11'})
		self._test_post_resource_invalid_field(client, resource_data, {'date': '11-08-2018'})

	def test_post_events_invalid_event_type(self, client, resource_data):
		'''Test POST /events API for event creation when event_type field is note a recognised value'''
		self._test_post_resource_invalid_field(client, resource_data, {'event_type': 'foo bar'})
		self._test_post_resource_invalid_field(client, resource_data, {'event_type': 'race'})

	def test_put_event_status(self, client, resource_fixture):
		"""Test PUT /events/{id} API for event status modification"""
		assert 'status' not in resource_fixture # test has default status
		event_status = {'state': 'cancelled', 'url': 'http://sorryaboutthat.com/notice'}
		self._test_put_resource_field(client, resource_fixture, ('status', event_status))

class TestOneDayEvents(TestEvents):

	def test_post_one_day_event(self, client, resource_data, signon_data, stage_data):
		'''Test POST /events/ API for a OneDayEvent'''
		resource_data['sign_on'] = signon_data
		resource_data['races'] = [stage_data]
		self.test_post_resource(client, resource_data)

	def _test_post_invalid_one_day_event(self, client, resource_data, stage_data):
		"""Test POST /events/{id} API for invalid event stage data"""
		stage_data['stage_type'] = 'tricycle race'
		self._test_post_resource_invalid_field(client, resource_data, {'races': [stage_data]})

	def test_add_race(self, client, resource_fixture, stage_data):
		"""Test PUT /events/{id} API for adding a race to an event that doesn't yet have any races"""
		races = []
		stage_data['eligible_categories'] = ['A3']
		stage_data['title'] = 'A3 race'
		races.append(stage_data)
		self._test_put_resource_field(client, resource_fixture, ('races', races))
