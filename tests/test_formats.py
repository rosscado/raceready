import pytest
from context import formats
from isodate.isoerror import ISO8601Error

def test_is_spacetime():
	# valid inputs
	assert formats.is_spacetime('2018-09-06 13:40')
	assert formats.is_spacetime('2018/09/06 13:40')
	assert formats.is_spacetime('2018-09-06T13:40')
	assert formats.is_spacetime('2018-09-06 13:40:30')
	# invalid inputs
	assert_is_not_spacetime('foo bar')
	assert_is_not_spacetime('Tuesday 6th September 2018, 13:40')

def assert_is_not_spacetime(value):
	with pytest.raises(ISO8601Error):
		formats.is_spacetime(value)
