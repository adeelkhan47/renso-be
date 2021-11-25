from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.payment_method import PaymentMethod
from model.payment_tax import PaymentTax
from . import api, schema


@api.route("")
class PaymentMethodList(Resource):
    @api.doc("Get all payment methods")
    @api.marshal_list_with(schema.get_list_response)
    def get(self):
        args = request.args
        all_rows, count = PaymentMethod.filtration(args)
        return response_structure(all_rows, count), 200

    @api.param("name", required=True)
    @api.param("tax_ids", required=True)
    def post(self):
        name = request.args.get("name")
        pay = PaymentMethod(name, "Active")
        pay.insert()
        all_tax_ids = request.args.get("tax_ids").split(",")
        for each in all_tax_ids:
            PaymentTax(each, pay.id).insert()

        return "ok", 201


@api.route("/<int:payment_method_id>")
class Payment_Method_by_id(Resource):
    @api.doc("Get Widget by id")
    @api.marshal_list_with(schema.get_by_id_response)
    def get(self, payment_method_id):
        lan = PaymentMethod.query_by_id(payment_method_id)
        return response_structure(lan), 200

    @api.doc("Delete method by id")
    def delete(self, payment_method_id):
        PaymentMethod.delete(payment_method_id)
        return "ok", 200
