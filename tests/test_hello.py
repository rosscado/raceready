import pytest

from hello import hello

@pytest.fixture
def client():
	hello.app.config['TESTING'] = True
	client = hello.app.test_client()

	yield client
