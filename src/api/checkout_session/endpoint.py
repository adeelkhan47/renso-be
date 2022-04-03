from http import HTTPStatus
from pathlib import Path

import jinja2
from flask import request, redirect
from flask_restx import Resource

from common.email_service import send_email
from common.helper import error_message, response_structure
from configuration import configs
from model.associate_email import AssociateEmail
from model.order import Order
from model.order_status import OrderStatus
from service.stripe_service import Stripe
from . import api, schema

TEMPLATE_PATH = str(Path(__file__).parent.parent.parent) + "/templates"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader([TEMPLATE_PATH, "../templates/"]),
    autoescape=jinja2.select_autoescape(),
)


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
        template = env.get_template("receipt.html")
        stuff_to_render = template.render(
            configs=configs,
            actual_total_price=order.actual_total_cost,
            effected_total_price=order.effected_total_cost,
            order=order,
            total=order.total_cost,
            tax_amount=order.tax_amount
        )
        send_email(order.client_email, "Order Confirmation", stuff_to_render)
        emails, count = AssociateEmail.filtration({"status:eq": "true"})
        bookings_to_check = [x.booking for x in order.order_bookings]
        association_data = {}
        for each in emails:
            item_subtypes = [x.item_subtype for x in each.associate_email_subtypes]
            for booking in bookings_to_check:
                if booking.item.item_subtype in item_subtypes:
                    if each.email not in association_data.keys():
                        association_data[each.email] = []
                    association_data[each.email].append(booking)
        template2 = env.get_template("associate_receipt.html")
        for email in association_data.keys():
            stuff_to_render2 = template2.render(
                configs=configs,
                bookings=association_data[email]
            )
            send_email(email, "Order Confirmation for Associations", stuff_to_render2)

        order_status_id = OrderStatus.get_id_by_name("Paid")
        Order.update(order_id, {"order_status_id": order_status_id})
        if session_id:
            #return redirect(f"{configs.FRONT_END_URL}success", code=200)
            return redirect('https://google.com')
        return redirect(f"{configs.FRONT_END_URL}failure", code=400)
