from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.user import User
from . import api, schema


@api.route("")
class user_list(Resource):
    @api.doc("Get all users")
    @api.marshal_list_with(schema.get_list_responseUser)
    def get(self):
        args = request.args
        all_users, count = User.filtration(args)
        return response_structure(all_users, count), 200

    @api.param("name", required=True)
    @api.param("password", required=True)
    @api.param("email", required=True)
    @api.param("subscription", required=True)
    @api.param("status", required=True, type=int)
    @api.marshal_list_with(schema.get_list_responseUser)
    def post(self):
        name = request.args.get("name")
        password = request.args.get("password")
        email = request.args.get("email")
        subscription = request.args.get("subscription")
        status = bool(request.args.get("status"))
        user = User(name, email, password, subscription, status)
        user.insert()
        return response_structure(User.query_by_id(user.id)), 201


@api.route("/login")
class user_by_id(Resource):
    @api.param("password", required=True)
    @api.param("email", required=True)
    @api.marshal_list_with(schema.get_list_responseUser)
    def post(self):
        args = {}
        args["email:eq"] = request.args.get("email")
        args["password:eq"] = request.args.get("password")
        all_users, count = User.filtration(args)
        if count >= 1:
            return response_structure(all_users[0]), 200
        else:
            return "User not found with these credentials", 404


@api.route("/<int:user_id>")
class user_by_id(Resource):
    @api.doc("Get user by id")
    @api.marshal_list_with(schema.get_by_id_responseUser)
    def get(self, user_id):
        user = User.query_by_id(user_id)
        return response_structure(user), 200

    @api.doc("Delete user by id")
    def delete(self, user_id):
        User.delete(user_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseUser, skip_none=True)
    @api.param("name")
    @api.param("password")
    @api.param("email")
    @api.param("subscription")
    @api.param("status", type=int)
    def patch(self, user_id):
        data = request.args
        if "status" in data.keys():
            data["status"] = bool(data["status"])
        User.update(user_id, request.args)
        user = User.query_by_id(user_id)
        return response_structure(user), 200
