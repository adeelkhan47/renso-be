from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.language import Language
from . import api, schema


@api.route("")
class LanguageList(Resource):
    @api.doc("Get all Languages")
    @api.marshal_list_with(schema.get_list_responseLanguage)
    def get(self):
        args = request.args
        all_rows, count = Language.filtration(args)
        return response_structure(all_rows, count), 200

    @api.marshal_list_with(schema.get_by_id_responseLanguage)
    @api.param("name", required=True)
    def post(self):
        payload = api.payload
        name = payload.get("name")
        lan = Language(name, "Active")
        lan.insert()
        return response_structure(lan), 201


@api.route("/<int:language_id>")
class Language_by_id(Resource):
    @api.doc("Get Widget by id")
    @api.marshal_list_with(schema.get_by_id_responseLanguage)
    def get(self, language_id):
        lan = Language.query_by_id(language_id)
        return response_structure(lan), 200

    @api.doc("Delete Widget by id")
    def delete(self, language_id):
        Language.delete(language_id)
        return "ok", 200
