from datetime import datetime

from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure
from model.booking import Booking
from model.custom_data import CustomData
from model.custom_parameter import CustomParameter
from model.order import Order
from model.order_bookings import OrderBookings
from model.order_custom_data import OrderCustomData
from model.order_status import OrderStatus
from service.stripe_service import Stripe

from . import api, schema


@api.route("")
class order_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseOrder)
    def get(self):
        args = request.args
        all_items, count = Order.filtration(args)
        return response_structure(all_items, count), 200

    @api.marshal_list_with(schema.get_by_id_responseOrder_with_session, skip_none=True)
    @api.expect(schema.Order_Expect)
    def post(self):
        payload = api.payload
        parameters, count = CustomParameter.filtration({})
        custom_parameters = [each.name for each in parameters]

        client_name = payload.get("client_name")
        client_email = payload.get("client_email")
        order_status_id = OrderStatus.get_id_by_name("Payment Pending")
        phone_number = payload.get("phone_number")
        time_period = payload.get("time_period")
        all_booking_ids = payload.get("booking_ids").split(",")
        total_cost = payload.get("total_cost")
        order = Order(client_name, client_email, phone_number, order_status_id, time_period, total_cost)
        order.insert()
        for each in payload.keys():
            if each in custom_parameters:
                customData = CustomData(each, payload.get(each))
                customData.insert()
                OrderCustomData(customData.id, order.id).insert()
        for each in all_booking_ids:
            OrderBookings(each, order.id).insert()
        # strip_part
        product_id = Stripe.create_product(
            f"{str(order.id)}_{client_name}_{str(total_cost)}_{str(datetime.now())}")
        price_id = Stripe.create_price(product_id, total_cost)
        session_id = Stripe.create_checkout_session(price_id, order.id)
        response_data = {"order": order, "session_id": session_id}
        return response_structure(response_data), 201


@api.route("/<int:order_id>")
class order_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseOrder)
    def get(self, order_id):
        order = Order.query_by_id(order_id)
        if not order:
            raise NotFound("Item Not Found.")
        return response_structure(order), 200

    @api.doc("Delete item by id")
    def delete(self, order_id):
        Order.delete(order_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseOrder, skip_none=True)
    @api.expect(schema.Order_Expect)
    def patch(self, order_id):
        data = api.payload.copy()

        if "order_status_id" in data.keys() and int(data["order_status_id"]) == OrderStatus.get_id_by_name("Completed"):
            order = Order.query_by_id(order_id)
            for each in order.order_bookings:
                Booking.close_booking(each.booking.id)

        if "booking_ids" in data.keys():
            all_booking_ids = api.payload.get("booking_ids").split(",")
            total_cost = 0.0
            for booking_id in all_booking_ids:
                booking = Booking.query_by_id(booking_id)
                if not booking:
                    raise NotFound(f"Item_id {booking_id} no found.")
                diff = booking.end_time - booking.start_time
                days, seconds = diff.days, diff.seconds
                hours = days * 24 + seconds // 3600
                item_price = float(booking.item.item_subtype.price) * float(hours)
                cost = item_price * (100 - booking.discount) / 100
                total_cost += cost
            del data["booking_ids"]
            data["total_cost"] = cost
            OrderBookings.delete_by_order_id(order_id)
            for each in all_booking_ids:
                OrderBookings(each, order_id).insert()
        Order.update(order_id, data)
        order = Order.query_by_id(order_id)
        return response_structure(order), 200


@api.route("/by_item_type/<int:item_type_id>")
class order_by_id(Resource):
    @api.marshal_list_with(schema.get_list_responseOrder)
    def get(self, item_type_id):
        args = request.args
        orders_query = Order.getQuery_OrderByItemType(item_type_id)
        allorders, rows = Order.filtration(args, orders_query)
        return response_structure(allorders, rows), 200


@api.route("/by_item_subtype/<int:item_subtype_id>")
class order_by_item_subtype_id(Resource):
    @api.marshal_list_with(schema.get_list_responseOrder)
    def get(self, item_subtype_id):
        args = request.args
        orders_query = Order.getQuery_OrderByItemSubType(item_subtype_id)
        allorders, rows = Order.filtration(args, orders_query)
        return response_structure(allorders, rows), 200
