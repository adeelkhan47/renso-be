from flask import g
from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure
from decorator.authorization import auth
from model.associate_email import AssociateEmail
from model.associate_email_subtypes import AssociateEmailSubtype
from . import api, schema


@api.route("")
class AssociateEmailList(Resource):
    @api.doc("Get all associate_email")
    @api.marshal_list_with(schema.get_list_responseAssociateEmail)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        all_rows, count = AssociateEmail.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.AssociateEmail_Expect)
    @api.marshal_list_with(schema.get_by_id_responseAssociateEmail)
    @auth
    def post(self):
        payload = api.payload
        item_type_ids = payload.get("item_type_ids").split(",")
        associateEmail = AssociateEmail(payload.get("email"), payload.get("status"), g.current_user.id)
        associateEmail.insert()
        for each in item_type_ids:
            if each:
                AssociateEmailSubtype(associateEmail.id, each).insert()
        return response_structure(associateEmail), 201


@api.route("/<int:associate_email_id>")
class voucher_by_id(Resource):
    @api.doc("Get associate_email_id")
    @api.marshal_list_with(schema.get_by_id_responseAssociateEmail)
    @auth
    def get(self, associate_email_id):
        associateEmail = AssociateEmail.query_by_id(associate_email_id)
        if not associateEmail:
            raise NotFound("Item Not Found.")
        return response_structure(associateEmail), 200

    @api.doc("Delete method by id")
    @auth
    def delete(self, associate_email_id):
        AssociateEmail.delete(associate_email_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseAssociateEmail)
    @api.expect(schema.AssociateEmail_Expect)
    @auth
    def patch(self, associate_email_id):
        data = api.payload.copy()
        if "item_type_ids" in data.keys():
            AssociateEmailSubtype.delete_by_email_id(associate_email_id)
            item_type_ids = data.get("item_type_ids").split(",")
            for each in item_type_ids:
                if each:
                    AssociateEmailSubtype(associate_email_id, each).insert()
            del data["item_type_ids"]
        AssociateEmail.update(associate_email_id, data)
        associateEmail = AssociateEmail.query_by_id(associate_email_id)
        return response_structure(associateEmail), 200
