from flask_restx import Resource
from . import schema, api


@api.route("")
class user_list(Resource):
    @api.doc("Get all accounts")
    def get(self):
        return "Hello", 200