from datetime import datetime

from flask import g, redirect
from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure
from decorator.authorization import auth
from model.booking import Booking
from model.cart import Cart
from model.custom_data import CustomData
from model.custom_parameter import CustomParameter
from model.front_end_configs import FrontEndCofigs
from model.order import Order
from model.order_bookings import OrderBookings
from model.order_custom_data import OrderCustomData
from model.order_status import OrderStatus
from model.payment_method import PaymentMethod
from model.voucher import Voucher
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
    @api.expect(schema.Order_Expect)
    @auth
    def post(self):
        payload = api.payload.copy()
        parameters, count = CustomParameter.filtration({})
        custom_parameters = [each.name for each in parameters]

        client_name = payload.get("client_name")
        client_email = payload.get("client_email")
        order_status_id = OrderStatus.get_id_by_name("Payment Pending")
        phone_number = payload.get("phone_number")
        cart = Cart.query_by_id(payload.get("cart_id"))
        bookings = [each.booking for each in cart.cart_bookings]

        ##
        price_factor = 100
        if "voucher" in payload.keys() and payload.get("voucher"):
            voucher = Voucher.get_voucher_by_code(payload.get("voucher"), g.current_user.id)
            if voucher:
                price_factor = voucher.price_factor
        payment_method = PaymentMethod.get_payment_method_by_name("Stripe", g.current_user.id)
        actual_total_price = 0
        effected_total_price = 0
        for booking in bookings:
            actual_total_price += booking.cost
            effected_total_price += (price_factor / 100) * booking.cost

        tax_amount = 0
        if payment_method:
            for each in payment_method.payment_tax:
                tax = each.tax
                tax_amount += tax.percentage / 100 * effected_total_price

        actual_total_price_after_tax = effected_total_price + tax_amount

        ##

        order = Order(client_name, client_email, phone_number, order_status_id,
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
        if actual_total_price_after_tax > 0:
            product_id = Stripe.create_product(
                f"{str(order.id)}_{client_name}_{str(actual_total_price_after_tax)}_{str(datetime.now())}")
            price_id = Stripe.create_price(product_id, actual_total_price_after_tax)
            session_id = Stripe.create_checkout_session(price_id, order.id)
            response_data = {"order": order, "session_id": session_id}
        else:
            process_order_completion(order)
            response_data = {"order": order, "session_id": None}
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
