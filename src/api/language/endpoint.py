from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.language import Language
from . import api, schema
from flask import g


@api.route("")
class LanguageList(Resource):
    @api.doc("Get all Languages")
    @api.marshal_list_with(schema.get_list_responseLanguage)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        args["is_deleted:eq"] = "False"
        all_rows, count = Language.filtration(args)
        return response_structure(all_rows, count), 200

    @api.marshal_list_with(schema.get_by_id_responseLanguage)
    @api.expect(schema.LanguageExpect)
    @auth
    def post(self):
        payload = api.payload
        name = payload.get("name")
        status = payload.get("status")
        lan = Language(name, status, g.current_user.id)
        lan.insert()
        return response_structure(lan), 201


@api.route("/<int:language_id>")
class Language_by_id(Resource):
    @api.doc("Get Widget by id")
    @api.marshal_list_with(schema.get_by_id_responseLanguage)
    @auth
    def get(self, language_id):
        lan = Language.query_by_id(language_id)
        return response_structure(lan), 200

    @auth
    @api.doc("Delete Widget by id")
    def delete(self, language_id):
        Language.soft_delete(language_id)
        return "ok", 200
