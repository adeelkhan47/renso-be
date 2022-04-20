import hashlib

from flask import g
from flask import request
from flask_restx import Resource

from common.helper import response_structure, error_message
from decorator.authorization import auth
from model.front_end_configs import FrontEndCofigs
from model.item_type import ItemType
from model.payment_method import PaymentMethod
from model.tag import Tag
from model.user import User
from . import api, schema


@api.route("")
class user_list(Resource):
    @api.doc("Get all users")
    @api.marshal_list_with(schema.get_list_responseUser)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_key:eq"] = g.current_user.user_key
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
        if User.get_by_email(email):
            return error_message("User with this email already exist."), 404
        user_key = hashlib.md5((email + subscription).encode()).hexdigest()
        user = User(name, email, password, subscription, image, gender, status, user_key)
        user.insert()
        FrontEndCofigs("", "http://www.front_end.com/", "dummy@strato.de", "EmailPassword",
                       "http://www.privacy_polcy.com/", user.id).insert()
        item_type = ItemType("Extra", 1, True, "", user.id)
        item_type.insert()
        Tag("Cheap", "", "blue", user.id).insert()
        Tag("Luxury", "", "green", user.id).insert()
        Tag("Old", "", "orange", user.id).insert()
        Tag("New", "", "red", user.id).insert()
        PaymentMethod("Stripe", True, user.id).insert()
        return response_structure(User.query_by_id(user.id)), 201


@api.route("/login")
class user_by_login_id(Resource):
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
            return error_message("User not found with these credentials"), 404


@api.route("/<int:user_id>")
class user_by_ind_id(Resource):
    @api.doc("Get user by id")
    @api.marshal_list_with(schema.get_by_id_responseUser)
    @auth
    def get(self, user_id):
        user = User.query_by_id(user_id)
        return response_structure(user), 200

    @auth
    @api.doc("Delete user by id")
    def delete(self, user_id):
        User.delete(user_id)
        return "ok", 200

    @auth
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
