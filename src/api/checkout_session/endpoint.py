import uuid
from http import HTTPStatus
from pathlib import Path

import jinja2
from flask import request, redirect
from flask_restx import Resource

from common.email_service import send_email
from common.helper import response_structure
from configuration import configs
from model.associate_email import AssociateEmail
from model.booking_status import BookingStatus
from model.email_text import EmailText
from model.front_end_configs import FrontEndCofigs
from model.item_type import ItemType
from model.order import Order
from model.order_backup import OrderBackUp
from model.order_status import OrderStatus
from model.voucher import Voucher
from service.paypal import PayPal
from service.stripe_service import Stripe
from . import api, schema

TEMPLATE_PATH = str(Path(__file__).parent.parent.parent) + "/templates"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader([TEMPLATE_PATH, "../templates/"]),
    autoescape=jinja2.select_autoescape(),
)


def create_email(order):
    actual_text = ""
    email_text = EmailText.get_by_user_id(order.user_id)
    custom_values_dict = {}
    custom_values = [x.custom_data for x in order.order_custom_data]
    for each in custom_values:
        custom_values_dict[each.name] = each.value
    if email_text:
        actual_text = email_text.text
        custom_variables = [t for t in actual_text.split() if t.startswith('$')]
        itemType_text_variables = [t for t in actual_text.split() if t.startswith('#')]
        for each in itemType_text_variables:
            item_type = ItemType.get_by_item_type_name(each[1:])
            if item_type and item_type.itemTypeTexts:
                data = item_type.itemTypeTexts[0].text
                actual_text = actual_text.replace(each, data)
            else:
                actual_text = actual_text.replace(each, "")
        actual_text = actual_text.replace("$name", order.client_name)
        for each in custom_variables:
            if each[1:] in custom_values_dict.keys():
                actual_text = actual_text.replace(each, custom_values_dict.get(each[1:]))
            else:
                actual_text = actual_text.replace(each, "")
    actual_text = actual_text.replace('\n', '<br>')
    return actual_text


def process_order_completion(order, language, order_backup_id):
    order_backup = OrderBackUp.query_by_id(order_backup_id)
    email_text = create_email(order)
    order_status_paid_id = OrderStatus.get_id_by_name("Paid")
    order_status_completed_id = OrderStatus.get_id_by_name("Completed")
    order_status_cancelled_id = OrderStatus.get_id_by_name("Cancelled")
    if language == "de":
        associate_receipt_template = "associate_receipt_de.html"
        receipt_template = "receipt_de.html"
    elif language == "en":
        associate_receipt_template = "associate_receipt_en.html"
        receipt_template = "receipt_en.html"
    else:
        associate_receipt_template = "associate_receipt_en.html"
        receipt_template = "receipt_en.html"
    app_configs = FrontEndCofigs.get_by_user_id(order.user_id)
    FE_URL = app_configs.front_end_url
    if order.order_status_id == order_status_paid_id:
        return redirect(f"{FE_URL}failure")
    if order.order_status_id == order_status_completed_id:
        return redirect(f"{FE_URL}failure")
    if order.order_status_id == order_status_cancelled_id:
        return redirect(f"{FE_URL}failure")
    template = env.get_template(receipt_template)

    stuff_to_render = template.render(
        configs=configs,
        actual_total_price=order.actual_total_cost,
        effected_total_price=order.effected_total_cost,
        order=order,
        total=order.total_cost,
        tax_amount=order.tax_amount,
        edit_unique_key=order_backup.unique_key,
        fe_url=FE_URL,
        email_text=email_text,
        footer_email=app_configs.email
    )

    send_email(order.client_email, "Order Confirmation", stuff_to_render, app_configs.email, app_configs.email_password)
    emails, count = AssociateEmail.filtration({"status:eq": "true", "user_id:eq": str(order.user_id)})
    bookings_to_check = [x.booking for x in order.order_bookings]
    association_data = {}
    for each in emails:
        item_subtypes = [x.item_subtype for x in each.associate_email_subtypes]
        for booking in bookings_to_check:
            if booking.item.item_subtype in item_subtypes:
                if each.email not in association_data.keys():
                    association_data[each.email] = []
                association_data[each.email].append(booking)
    template2 = env.get_template(associate_receipt_template)
    for email in association_data.keys():
        stuff_to_render2 = template2.render(
            configs=configs,
            bookings=association_data[email],
            footer_email=app_configs.email
        )
        send_email(email, "Order Confirmation for Associations", stuff_to_render2, app_configs.email,
                   app_configs.email_password)
    Order.update(order.id, {"order_status_id": order_status_paid_id})
    active_booking_status = BookingStatus.get_id_by_name("Active")
    for each in order.order_bookings:
        each.booking.update(each.booking.id, {"booking_status_id": active_booking_status})


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
    # @api.marshal_with(schema.CheckOutSessionResponse, skip_none=True)
    @api.param("session_id")
    @api.param("order_id")
    def get(self):
        """
        Stripe Payment Failed


        :return:
        """
        order_status_Cancelled_id = OrderStatus.get_id_by_name("Cancelled")
        args = request.args
        order_id = args["order_id"]
        order = Order.query_by_id(int(order_id))
        app_configs = FrontEndCofigs.get_by_user_id(order.user_id)

        FE_URL = app_configs.front_end_url
        Order.update(order.id, {"order_status_id": order_status_Cancelled_id})
        return redirect(f"{FE_URL}checkout")
        # return error_message("TopUp Failed"), HTTPStatus.BAD_REQUEST


@api.route("/success")
class CheckOutSessionSuccess(Resource):
    @api.doc("Accept Success for checkout")
    # @api.marshal_with(schema.CheckOutSessionResponseSuccess, skip_none=True)
    @api.param("session_id", required=False)
    @api.param("order_id")
    @api.param("paymentId", required=False)
    @api.param("voucher_code")
    @api.param("language")
    def get(self):
        payment_method = "Stripe"
        args = request.args
        session_id = args["session_id"]
        voucher_code = args["voucher_code"]
        payment_reference = session_id
        if session_id == "notStripe":
            payment_method = "Paypal"
            payment_reference = args["paymentId"]
            PayPal.execute_payment(args["paymentId"], args["PayerID"])

        order_id = args["order_id"]
        language = args["language"]
        order = Order.query_by_id(int(order_id))
        unique_key = uuid.uuid4()
        if voucher_code:
            voucher = Voucher.get_voucher_by_code(voucher_code, order.user_id)
            if voucher:
                if not voucher.counter:
                    Voucher.update(voucher.id, {"counter": 0})
                Voucher.update(voucher.id, {"counter": voucher.counter + 1})
        order_backup = OrderBackUp(order.cart_id, str(unique_key), payment_method, payment_reference, voucher_code,
                                   str(order.total_cost))
        order_backup.insert()
        process_order_completion(order, language, order_backup.id)
        app_configs = FrontEndCofigs.get_by_user_id(order.user_id)
        FE_URL = app_configs.front_end_url

        if session_id:
            return redirect(f"{FE_URL}success")
        return redirect(f"{FE_URL}failure")
