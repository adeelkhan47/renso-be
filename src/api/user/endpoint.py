from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

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

    @api.expect(schema.userPostExpect, validate=True)
    @api.marshal_list_with(schema.get_by_id_responseUser)
    def post(self):
        payload = api.payload
        name = payload.get("name")
        password = payload.get("password")
        email = payload.get("email")
        subscription = payload.get("subscription")
        image = payload.get("image")
        gender = payload.get("gender")
        status = payload.get("status")
        user = User(name, email, password, subscription, image, gender, status)
        user.insert()
        return response_structure(User.query_by_id(user.id)), 201


@api.route("/login")
class user_by_id(Resource):

    @api.expect(schema.userLoginPostExpect)
    @api.marshal_list_with(schema.get_by_id_responseUser)
    def post(self):
        args = {}
        payload = api.payload
        args["email:eq"] = payload["email"]
        args["password:eq"] = payload["password"]
        all_users, count = User.filtration(args)
        if count >= 1:
            return response_structure(all_users[0]), 200
        else:
            raise NotFound("User not found with these credentials")


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
    @api.expect(schema.userPostExpect, validate=True)
    def patch(self, user_id):
        payload = api.payload
        data = payload.copy()
        if "status" in data.keys():
            data["status"] = bool(data["status"])
        User.update(user_id, data)
        user = User.query_by_id(user_id)
        return response_structure(user), 200
