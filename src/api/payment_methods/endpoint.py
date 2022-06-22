from flask import g
from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.payment_method import PaymentMethod
from model.payment_tax import PaymentTax
from . import api, schema


@api.route("")
class PaymentMethodList(Resource):
    @api.doc("Get all payment methods")
    @api.marshal_list_with(schema.get_list_responsePaymentMethod)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        all_rows, count = PaymentMethod.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.PaymentMethodExpect)
    @api.marshal_list_with(schema.get_by_id_responsePaymentMethod)
    @auth
    def post(self):
        payload = api.payload
        name = payload.get("name")
        description = payload.get("description")
        status = payload.get("status")
        pay = PaymentMethod(name, description, bool(status), g.current_user.id)
        pay.insert()
        all_tax_ids = payload.get("tax_ids").split(",")
        for each in all_tax_ids:
            if each:
                PaymentTax(each, pay.id).insert()
        return response_structure(pay), 201


@api.route("/<int:payment_method_id>")
class Payment_Method_by_id(Resource):
    @api.doc("Get Widget by id")
    @api.marshal_list_with(schema.get_by_id_responsePaymentMethod)
    @auth
    def get(self, payment_method_id):
        lan = PaymentMethod.query_by_id(payment_method_id)
        return response_structure(lan), 200

    @api.doc("Delete method by id")
    @auth
    def delete(self, payment_method_id):
        PaymentMethod.delete(payment_method_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responsePaymentMethod, skip_none=True)
    @api.expect(schema.PaymentMethodExpect)
    @auth
    def patch(self, payment_method_id):
        payload = api.payload
        data = payload.copy()
        if "status" in data.keys():
            data["status"] = bool(data["status"])

        if "tax_ids" in data.keys():
            PaymentTax.delete_by_payment_id(payment_method_id)
            tax_ids = data.get("tax_ids").split(",")
            for each in tax_ids:
                if each:
                    PaymentTax(payment_id=payment_method_id, tax_id=each).insert()
            del data["tax_ids"]
        payment_method = PaymentMethod.query_by_id(payment_method_id)
        PaymentMethod.update(payment_method_id, data)
        return response_structure(payment_method), 200
