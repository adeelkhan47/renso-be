import uuid
from datetime import datetime

from flask import g
from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound, BadRequest

from common.helper import response_structure, create_pdf_and_send_email
from decorator.authorization import auth
from model.booking import Booking
from model.booking_status import BookingStatus
from model.cart import Cart
from model.custom_data import CustomData
from model.custom_parameter import CustomParameter
from model.order import Order
from model.order_backup import OrderBackUp
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
        order_status_Updated_id = OrderStatus.get_id_by_name("Updated")
        booking_status_payment_pending_id = BookingStatus.get_id_by_name("Payment Pending")
        phone_number = payload.get("phone_number")
        language = "en"
        edit = False
        order_backup = None
        if "language" in payload.keys():
            language = payload.get("language")
        if "backup_unique_key" in payload.keys() and payload.get("backup_unique_key"):
            order_backup = OrderBackUp.get_order_backUp_by_unique_key(payload.get("backup_unique_key"))
            if order_backup:
                edit = True
            else:
                raise BadRequest("Invalid Request")
        cart = Cart.query_by_id(payload.get("cart_id"))
        bookings = [each.booking for each in cart.cart_bookings]

        ##
        price_factor = 100
        voucher_code = ""
        if not edit:
            if "voucher" in payload.keys() and payload.get("voucher"):
                voucher = Voucher.get_voucher_by_code(payload.get("voucher"), g.current_user.id)
                if voucher:
                    voucher_code = voucher.code
                    price_factor = voucher.price_factor
        else:
            voucher = Voucher.get_voucher_by_code(order_backup.voucher, g.current_user.id)
            if voucher:
                voucher_code = voucher.code
                price_factor = voucher.price_factor
        payment_method = PaymentMethod.query_by_id(payment_method_id)
        price = sum([booking.cost for booking in bookings]) if bookings else 0
        final_price = (price_factor / 100) * price
        ##
        # update old order
        previous_orders = Order.get_order_by_cart_id(cart.id)
        for each_old_order in previous_orders:
            Order.update(each_old_order.id, {"order_status_id": order_status_Updated_id})
        ##
        if not edit:
            order = Order(client_name, client_email, phone_number, order_status_payment_pending_id,
                          round(final_price, 2), cart.id, round(price, 2),
                          round(final_price, 2), round(0, 2), g.current_user.id)
        else:
            edited_price = final_price - round(float(order_backup.price_paid), 2)
            if edited_price < 0:
                edited_price = 0
            order = Order(client_name, client_email, phone_number, order_status_payment_pending_id,
                          round(edited_price, 2), cart.id, round(price, 2),
                          round(edited_price, 2), round(0, 2), g.current_user.id)
        order.insert()
        for each in payload.keys():
            if each in custom_parameters:
                customData = CustomData(each, payload.get(each))
                customData.insert()
                OrderCustomData(customData.id, order.id).insert()
        for each in bookings:
            Booking.update(each.id, {"booking_status_id": booking_status_payment_pending_id})
            OrderBookings(each.id, order.id).insert()

        session_id = None
        paypal_url = None
        if not edit:
            order_name = f"{str(order.id)}_{client_name}_{str(final_price)}_{str(datetime.now())}"
        else:
            order_name = f"EDITED-{str(order.id)}_{client_name}_{str(final_price)}_{str(datetime.now())}"
        if payment_method.name == "Stripe":
            if order.total_cost > 0:

                product_id = Stripe.create_product(order_name)

                price_id = Stripe.create_price(product_id, order.total_cost)
                session_id = Stripe.create_checkout_session(price_id, order.id, language, voucher_code)
            else:
                unique_key = uuid.uuid4()
                order_backup = OrderBackUp(order.cart_id, str(unique_key), "Stripe", "None",
                                           voucher_code,
                                           str(order.total_cost))
                order_backup.insert()
                process_order_completion(order, language, order_backup.id,voucher_code)
        elif payment_method.name == "Paypal":
            if order.total_cost > 0:
                paypal_url = PayPal.create_paypal_session(order_name, order.id, language, voucher_code)
                if not paypal_url:
                    raise BadRequest("Paypal not working.")
            else:
                unique_key = uuid.uuid4()
                order_backup = OrderBackUp(order.cart_id, str(unique_key), "Paypal", "None",
                                           voucher_code,
                                           str(order.total_cost))
                order_backup.insert()
                process_order_completion(order, language, order_backup.id,voucher_code)

        else:
            raise NotFound("Payment_Method not Found.")
        response_data = {"order": order, "session_id": session_id, "paypal_url": paypal_url}
        return response_structure(response_data), 201


@api.route("/<int:order_id>")
class order_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseOrder)
    @auth
    def get(self, order_id):
        order = Order.query_by_id(order_id)
        create_pdf_and_send_email(order)
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
            create_pdf_and_send_email(order)
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
