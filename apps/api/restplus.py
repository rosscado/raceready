from flask_restplus import Api
from api.formats import CustomFormatChecker

# Notes on request payload input validation:
## Api(validate=True) enforces @api.expect(validate=True) everywhere
## see https://flask-restplus.readthedocs.io/en/stable/swagger.html#the-api-expect-decorator

api = Api(validate=True, format_checker=CustomFormatChecker())
