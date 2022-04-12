from flask import g
from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.tax import Tax
from . import api, schema


@api.route("")
class TaxList(Resource):
    @api.doc("Get all Tax")
    @api.marshal_list_with(schema.get_list_responseTax)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = g.current_user.id
        all_rows, count = Tax.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.Tax_expect)
    @api.marshal_list_with(schema.get_by_id_responseTax)
    @auth
    def post(self):
        payload = api.payload
        name = payload.get("name")
        percentage = payload.get("percentage")
        description = payload.get("description")
        tax = Tax(name, percentage, description, g.current_user.id)
        tax.insert()
        return response_structure(tax), 201


@api.route("/<int:tax_id>")
class tax_by_id(Resource):
    @api.doc("Get tax by id")
    @api.marshal_list_with(schema.get_by_id_responseTax)
    @auth
    def get(self, tax_id):
        tax = Tax.query_by_id(tax_id)
        return response_structure(tax), 200

    @api.doc("Delete method by id")
    @auth
    def delete(self, tax_id):
        Tax.delete(tax_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseTax, skip_none=True)
    @api.expect(schema.Tax_expect)
    @auth
    def patch(self, tax_id):
        payload = api.payload
        data = payload.copy()
        Tax.update(tax_id, data)
        tax = Tax.query_by_id(tax_id)
        return response_structure(tax), 200
