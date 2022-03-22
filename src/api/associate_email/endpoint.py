from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure
from model.associate_email import AssociateEmail

from . import api, schema


@api.route("")
class AssociateEmailList(Resource):
    @api.doc("Get all associate_email")
    @api.marshal_list_with(schema.get_list_responseAssociateEmail)
    def get(self):
        args = request.args
        all_rows, count = AssociateEmail.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.AssociateEmail_Expect)
    @api.marshal_list_with(schema.get_by_id_responseAssociateEmail)
    def post(self):
        payload = api.payload
        associateEmail = AssociateEmail(**payload)
        associateEmail.insert()
        return response_structure(associateEmail), 201


@api.route("/<int:associate_email_id>")
class voucher_by_id(Resource):
    @api.doc("Get associate_email_id")
    @api.marshal_list_with(schema.get_by_id_responseAssociateEmail)
    def get(self, associate_email_id):
        associateEmail = AssociateEmail.query_by_id(associate_email_id)
        if not associateEmail:
            raise NotFound("Item Not Found.")
        return response_structure(associateEmail), 200

    @api.doc("Delete method by id")
    def delete(self, associate_email_id):
        AssociateEmail.delete(associate_email_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseAssociateEmail)
    @api.expect(schema.AssociateEmail_Expect)
    def patch(self, associate_email_id):
        payload = api.payload
        AssociateEmail.update(associate_email_id, payload)
        associateEmail = AssociateEmail.query_by_id(associate_email_id)
        return response_structure(associateEmail), 200
