from jsonschema import FormatChecker
from isodate import parse_datetime

# custom fields
def parse_spacetime(spacetimestring):
	'''
	Parses ISO 8601 'YYYY-MM-DD HH:MM' date-times into datetime.datetime objects.
	'''
	datetimestring = spacetimestring.strip().replace(' ', 'T')
	return parse_datetime(datetimestring)

def is_spacetime(spacetimestring):
	return parse_spacetime(spacetimestring)


## format_checker=jsonschema.FormatChecker() enables date, date-time, and other validation
## when the appropriate module, e.g. isodate, is installed (`pip install isodate`)
## see https://python-jsonschema.readthedocs.io/en/v1.3.0/validate/#validating-formats

class CustomFormatChecker(FormatChecker):
	def __init__(self, *args, **kwargs):
		super(CustomFormatChecker, self).__init__(*args, **kwargs)
		if 'date-time' in self.checkers:
			# replace isodate date-time formatting function with our own
			default_date_checker = self.checkers['date-time']
			custom_date_checker = (is_spacetime, default_date_checker[1])
			self.checkers['date-time'] = custom_date_checker
