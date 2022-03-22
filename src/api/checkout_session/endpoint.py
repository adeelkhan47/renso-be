from http import HTTPStatus

from flask import request
from flask_restx import Resource

from common.helper import error_message, response_structure
from model.order import Order
from model.order_status import OrderStatus
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
    @api.param("order_id")
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
    @api.param("order_id")
    def get(self):
        args = request.args
        session_id = args["session_id"]
        order_id = args["order_id"]
        order = Order.query_by_id(order_id)
        order_status_id = OrderStatus.get_id_by_name("Paid")
        Order.update(order_id, {"order_status_id": order_status_id})
        if session_id:
            return response_structure({"msg": "TopUp Succeeded"}), HTTPStatus.OK
        return error_message("TopUp Failed"), HTTPStatus.BAD_REQUEST
