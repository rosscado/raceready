from flask_restplus import Api

# enforce @api.expect(validate=True) everywhere
# see https://flask-restplus.readthedocs.io/en/stable/swagger.html#the-api-expect-decorator
api = Api(validate=True)
