from datetime import datetime

from flask import g
from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound, BadRequest

from common.helper import response_structure
from decorator.authorization import auth
from model.booking import Booking
from model.cart import Cart
from model.custom_data import CustomData
from model.custom_parameter import CustomParameter
from model.order import Order
from model.order_bookings import OrderBookings
from model.order_custom_data import OrderCustomData
from model.order_status import OrderStatus
from model.payment_method import PaymentMethod
from model.voucher import Voucher
from service.paypal import PayPal
from service.stripe_service import Stripe
from . import api, schema
from ..checkout_session.endpoint import process_order_completion


@api.route("")
class order_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseOrder)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        all_items, count = Order.filtration(args)
        return response_structure(all_items, count), 200

    @api.marshal_with(schema.get_by_id_responseOrder_with_session, 201, skip_none=True)
    @api.expect(schema.Order_WithLanguage_Expect)
    @auth
    def post(self):
        payload = api.payload.copy()
        parameters, count = CustomParameter.filtration({})
        custom_parameters = [each.name for each in parameters]
        payment_method_id = payload.get("payment_method_id")
        client_name = payload.get("client_name")
        client_email = payload.get("client_email")
        order_status_payment_pending_id = OrderStatus.get_id_by_name("Payment Pending")
        phone_number = payload.get("phone_number")
        language = "en"
        if "language" in payload.keys():
            language = payload.get("language")
        cart = Cart.query_by_id(payload.get("cart_id"))
        bookings = [each.booking for each in cart.cart_bookings]

        ##
        price_factor = 100
        if "voucher" in payload.keys() and payload.get("voucher"):
            voucher = Voucher.get_voucher_by_code(payload.get("voucher"), g.current_user.id)
            if voucher:
                price_factor = voucher.price_factor
        payment_method = PaymentMethod.query_by_id(payment_method_id)
        actual_total_price = 0
        effected_total_price = 0
        taxs = []
        tax_amount = 0
        for booking in bookings:
            actual_total_price += booking.cost
            temp_tax_amount = 0
            for each in payment_method.payment_tax:
                if booking.item.item_subtype_id in [x.item_sub_type_id for x in each.tax.itemSubTypeTaxs]:
                    temp_tax_amount += (each.tax.percentage / 100) * booking.cost
                    if each.tax not in taxs:
                        taxs.append(each.tax)

            tax_amount += temp_tax_amount
            effected_total_price += (price_factor / 100) * booking.cost
        actual_total_price_after_tax = effected_total_price + tax_amount

        ##

        order = Order(client_name, client_email, phone_number, order_status_payment_pending_id,
                      round(actual_total_price_after_tax, 2), cart.id, round(actual_total_price, 2),
                      round(effected_total_price, 2), round(tax_amount, 2), g.current_user.id)
        order.insert()
        for each in payload.keys():
            if each in custom_parameters:
                customData = CustomData(each, payload.get(each))
                customData.insert()
                OrderCustomData(customData.id, order.id).insert()
        for each in bookings:
            OrderBookings(each.id, order.id).insert()
        # strip_part

        if payment_method.name == "Stripe":
            if actual_total_price_after_tax > 0:

                product_id = Stripe.create_product(
                    f"{str(order.id)}_{client_name}_{str(actual_total_price_after_tax)}_{str(datetime.now())}")

                price_id = Stripe.create_price(product_id, actual_total_price_after_tax)
                session_id = Stripe.create_checkout_session(price_id, order.id, language)
                response_data = {"order": order, "session_id": session_id, "paypal_url": None}
            else:
                process_order_completion(order, language)
                response_data = {"order": order, "session_id": None, "paypal_url": None}
        elif payment_method.name == "Paypal":
            if actual_total_price_after_tax > 0:
                paypal_url = PayPal.create_paypal_session(
                    f"{str(order.id)}_{client_name}_{str(actual_total_price_after_tax)}_{str(datetime.now())}",
                    order.id, language)
                if not paypal_url:
                    raise BadRequest("Paypal not working.")
                response_data = {"order": order, "session_id": None, "paypal_url": paypal_url}
            else:
                process_order_completion(order, language)
                response_data = {"order": order, "session_id": None}

        else:
            raise NotFound("Payment_Method not Found.")
        return response_structure(response_data), 201


@api.route("/<int:order_id>")
class order_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseOrder)
    @auth
    def get(self, order_id):
        order = Order.query_by_id(order_id)
        if not order:
            raise NotFound("Item Not Found.")
        return response_structure(order), 200

    @api.doc("Delete item by id")
    @auth
    def delete(self, order_id):
        order = Order.query_by_id(order_id)
        for each in order.order_bookings:
            Booking.cancel_booking(each.booking_id)
        Order.delete(order_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseOrder, skip_none=True)
    @api.expect(schema.Order_Expect)
    @auth
    def patch(self, order_id):
        data = api.payload.copy()
        if "order_status_id" in data.keys() and int(data["order_status_id"]) == OrderStatus.get_id_by_name("Completed"):
            order = Order.query_by_id(order_id)
            for each in order.order_bookings:
                Booking.close_booking(each.booking_id)
                # OrderBookings.delete_by_order_id(order_id)
        if "voucher" in data.keys():
            del data["voucher"]
        Order.update(order_id, data)
        order = Order.query_by_id(order_id)
        return response_structure(order), 200


@api.route("/by_item_type/<int:item_type_id>")
class order_by_id(Resource):
    @api.marshal_list_with(schema.get_list_responseOrder)
    @auth
    def get(self, item_type_id):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        orders_query = Order.getQuery_OrderByItemType(item_type_id)
        allorders, rows = Order.filtration(args, orders_query)
        return response_structure(allorders, rows), 200


@api.route("/by_item_subtype/<int:item_subtype_id>")
class order_by_item_subtype_id(Resource):
    @api.marshal_list_with(schema.get_list_responseOrder)
    @auth
    def get(self, item_subtype_id):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        orders_query = Order.getQuery_OrderByItemSubType(item_subtype_id)
        allorders, rows = Order.filtration(args, orders_query)
        return response_structure(allorders, rows), 200
