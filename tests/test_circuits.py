import pytest
from resource import ResourceTestCase
from context import app # check sys.path if this fails

arbitrary_url='https://www.mapmyride.com/routes/view/2189856949' # default circuit fixture url
arbitrary_distance_km=86.95
arbitrary_elevation_gain_m=1315

@pytest.fixture
def resource_name():
	return 'circuits'

@pytest.fixture
def resource_data():
	return {
		'url': arbitrary_url,
		'distance_km': arbitrary_distance_km,
        'elevation_gain_m': arbitrary_elevation_gain_m
	}

@pytest.fixture
def required_fields():
	return []


class TestCircuits(ResourceTestCase):
	# must declare ns fixture in this module to override dependent fixtures
	ns = '/api/{resources}/'.format(resources=resource_name())

	def test_has_flatness_index(self, client, resource_fixture):
		get_rv = client.get(self.ns)
		circuits = get_rv.get_json()
		for circuit in circuits:
			assert 'flatness_index' in circuit
