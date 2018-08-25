from flask_restplus import Api
from jsonschema import FormatChecker

# Notes on request payload input validation:
## Api(validate=True) enforces @api.expect(validate=True) everywhere
## see https://flask-restplus.readthedocs.io/en/stable/swagger.html#the-api-expect-decorator
#
## format_checker=jsonschema.FormatChecker() enables date, date-time, and other validation
## when the appropriate module, e.g. isodate, is installed (`pip install isodate`)
## see https://python-jsonschema.readthedocs.io/en/v1.3.0/validate/#validating-formats
api = Api(validate=True, format_checker=FormatChecker())
