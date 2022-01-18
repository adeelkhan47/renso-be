from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.payment_method import PaymentMethod
from model.payment_tax import PaymentTax
from . import api, schema


@api.route("")
class PaymentMethodList(Resource):
    @api.doc("Get all payment methods")
    @api.marshal_list_with(schema.get_list_responsePaymentMethod)
    def get(self):
        args = request.args
        all_rows, count = PaymentMethod.filtration(args)
        return response_structure(all_rows, count), 200

    @api.param("name", required=True)
    @api.param("status", required=True, type=int)
    @api.param("tax_ids", required=True)
    def post(self):
        payload = api.payload
        name = payload.get("name")
        status = payload.get("status")
        pay = PaymentMethod(name, bool(status))
        pay.insert()
        all_tax_ids = payload.get("tax_ids").split(",")
        for each in all_tax_ids:
            PaymentTax(each, pay.id).insert()
        return "ok", 201


@api.route("/<int:payment_method_id>")
class Payment_Method_by_id(Resource):
    @api.doc("Get Widget by id")
    @api.marshal_list_with(schema.get_by_id_responsePaymentMethod)
    def get(self, payment_method_id):
        lan = PaymentMethod.query_by_id(payment_method_id)
        return response_structure(lan), 200

    @api.doc("Delete method by id")
    def delete(self, payment_method_id):
        PaymentMethod.delete(payment_method_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responsePaymentMethod, skip_none=True)
    @api.param("name", )
    @api.param("status", type=int)
    @api.param("tax_ids")
    def patch(self, payment_method_id):
        payload = api.payload
        data = payload.copy()
        if "status" in data.keys():
            data["status"] = bool(data["status"])
        PaymentMethod.update(payment_method_id, data)
        payment_method = PaymentMethod.query_by_id(payment_method_id)
        return response_structure(payment_method), 200
