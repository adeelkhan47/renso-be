from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.tax import Tax
from . import api, schema


@api.route("")
class TaxList(Resource):
    @api.doc("Get all Tax")
    @api.marshal_list_with(schema.get_list_response)
    def get(self):
        args = request.args
        all_rows, count = Tax.filtration(args)
        return response_structure(all_rows, count), 200

    @api.param("name", required=True)
    @api.param("percentage", required=True)
    @api.param("description", required=True)
    def post(self):
        name = request.args.get("name")
        percentage = request.args.get("percentage")
        description = request.args.get("description")
        tax = Tax(name, percentage, description)
        tax.insert()
        return "ok", 201


@api.route("/<int:tax_id>")
class Payment_Method_by_id(Resource):
    @api.doc("Get tax by id")
    @api.marshal_list_with(schema.get_by_id_response)
    def get(self, tax_id):
        tax = Tax.query_by_id(tax_id)
        return response_structure(tax), 200

    @api.doc("Delete method by id")
    def delete(self, tax_id):
        Tax.delete(tax_id)
        return "ok", 200
