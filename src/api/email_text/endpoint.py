from flask import request, g
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.email_text import EmailText
from . import api, schema


@api.route("")
class EmailTextList(Resource):
    @api.doc("Get all EmailText")
    @api.marshal_list_with(schema.get_list_EmailText)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        all_rows, count = EmailText.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.EmailText_Expect)
    @api.marshal_list_with(schema.get_by_id_EmailText)
    @auth
    def post(self):
        payload = api.payload
        payload["user_id"] = g.current_user.id
        emailText = EmailText(**payload)
        emailText.insert()
        return response_structure(emailText), 201


@api.route("/<int:email_text_id>")
class EmailText_by_id(Resource):
    @api.doc("Get EmailText by id")
    @api.marshal_list_with(schema.get_by_id_EmailText)
    @auth
    def get(self, email_text_id):
        emailText = EmailText.query_by_id(email_text_id)
        return response_structure(emailText), 200

    @api.doc("Delete method by id")
    @auth
    def delete(self, email_text_id):
        EmailText.delete(email_text_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_EmailText)
    @api.expect(schema.EmailText_Expect)
    @auth
    def patch(self, email_text_id):
        payload = api.payload.copy()

        EmailText.update(email_text_id, payload)
        emailText = EmailText.query_by_id(email_text_id)
        return response_structure(emailText), 200
