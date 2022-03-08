from http import HTTPStatus

from flask import request
from flask_restx import Resource

from common.helper import response_structure, error_message
from service.stripe_service import Stripe
from . import api, schema


@api.route("")
class CheckOutSession(Resource):
    @api.doc("Create Stripe Session for checkout")
    @api.expect(schema.CreateSessionExpect, validate=True, strict=True)
    @api.marshal_with(schema.CheckOutSessionResponse, skip_none=True)
    def post(self):
        args = api.payload
        product_name = args["product_name"]
        price = args["price"]
        product_id = Stripe.create_product(product_name)
        price_id = Stripe.create_price(product_id, price)
        session_id = Stripe.create_checkout_session(price_id)
        response_obj = {"session_id": session_id}
        return response_structure(response_obj), HTTPStatus.CREATED


@api.route("/failed")
class CheckOutSessionFailed(Resource):
    @api.doc("Accept Success for checkout")
    @api.marshal_with(schema.CheckOutSessionResponse, skip_none=True)
    @api.param("session_id")
    def get(self):
        """
        Stripe Payment Failed

        :return:
        """
        return error_message("TopUp Failed"), HTTPStatus.BAD_REQUEST


@api.route("/success")
class CheckOutSessionSuccess(Resource):
    @api.doc("Accept Success for checkout")
    @api.marshal_with(schema.CheckOutSessionResponseSuccess, skip_none=True)
    @api.param("session_id")
    def get(self):
        args = request.args
        session_id = args["session_id"]
        if session_id:
            return response_structure({"msg": "TopUp Succeeded"}), HTTPStatus.OK
        return error_message("TopUp Failed"), HTTPStatus.BAD_REQUEST
