from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.user import User
from . import api, schema


@api.route("")
class user_list(Resource):
    @api.doc("Get all users")
    @api.marshal_list_with(schema.get_list_response)
    def get(self):
        args = request.args
        all_users, count = User.filtration(args)
        return response_structure(all_users, count), 200

    @api.param("name", required=True)
    @api.param("password", required=True)
    @api.param("email", required=True)
    def post(self):
        name = request.args.get("name")
        password = request.args.get("password")
        email = request.args.get("email")
        user = User(name, password, email, "Basic", "Active")
        user.insert()
        return "ok", 201


@api.route("/<int:user_id>")
class user_by_id(Resource):
    @api.doc("Get user by id")
    @api.marshal_list_with(schema.get_by_id_response)
    def get(self, user_id):
        user = User.query_by_id(user_id)
        return response_structure(user), 200

    @api.doc("Delete user by id")
    def delete(self, user_id):
        User.delete(user_id)
        return "ok", 200
