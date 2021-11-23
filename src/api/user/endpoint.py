from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.user import User
from . import api, schema


@api.route("")
class user_list(Resource):
    @api.doc("Get all accounts")
    @api.marshal_list_with(schema.get_list_response)
    def get(self):
        args = request.args
        all_users, count = User.filtration(args)
        return response_structure(all_users, count), 200

    @api.param("first_name", "First Name", required=True)
    @api.param("last_name", "Last Name", required=True)
    @api.param("email", "Email", required=True)
    def post(self):
        first_name = request.args.get("first_name")
        last_name = request.args.get("last_name")
        email = request.args.get("email")
        user = User(first_name, last_name, email)
        user.insert()
        print(user.id)
        return "ok", 201


@api.route("/<int:user_id>")
class user_by_id(Resource):
    @api.doc("Get all accounts")
    @api.marshal_list_with(schema.get_by_id_response)
    def get(self, user_id):
        user = User.query_by_id(user_id)
        return response_structure(user), 200
