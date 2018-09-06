import pytest
from resource import ResourceTestCase

arbitrary_title='Unit test club' # default club fixture title
arbitrary_url='http://www.clontarfcc.com/' # default club fixture url

@pytest.fixture
def resource_name():
	return 'clubs'

@pytest.fixture
def resource_data():
	return {
		'title': arbitrary_title,
		'url': arbitrary_url
	}

@pytest.fixture
def required_fields():
	return ['title']

class TestClubs(ResourceTestCase):
	# must declare ns fixture in this module to override dependent fixtures
	ns = '/api/{resources}/'.format(resources=resource_name())
