from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.custom_parameter import CustomParameter
from . import api, schema
from flask import g


@api.route("")
class CustomParameterList(Resource):
    @api.doc("Get all Custom Parameters")
    @api.marshal_list_with(schema.get_list_CustomParameter)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        all_rows, count = CustomParameter.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.CustomParameterExpect)
    @api.marshal_list_with(schema.get_by_id_CustomParameter)
    @auth
    def post(self):
        payload = api.payload
        name = payload.get("name")
        customParameter = CustomParameter(name, g.current_user.id)
        customParameter.insert()
        return response_structure(customParameter), 201


@api.route("/<int:custom_parameter_id>")
class CustomParameter_by_id(Resource):
    @api.doc("Get  by id")
    @api.marshal_list_with(schema.get_by_id_CustomParameter)
    @auth
    def get(self, custom_parameter_id):
        customParameter = CustomParameter.query_by_id(custom_parameter_id)
        return response_structure(customParameter), 200

    @api.doc("Delete method by id")
    @auth
    def delete(self, custom_parameter_id):
        CustomParameter.delete(custom_parameter_id)
        return "ok", 200
