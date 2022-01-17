from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure, error_message
from model.booking import Booking
from model.order import Order
from model.order_bookings import OrderBookings
from model.order_status import OrderStatus
from . import api, schema


@api.route("")
class order_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseOrder)
    def get(self):
        args = request.args
        all_items, count = Order.filtration(args)
        return response_structure(all_items, count), 200

    @api.marshal_list_with(schema.get_by_id_responseOrder, skip_none=True)
    @api.param("client_name", required=True)
    @api.param("status_id", required=True)
    @api.param("client_email", required=True)
    @api.param("phone_number", required=True)
    @api.param("time_period", required=True)
    @api.param("booking_ids", required=True)
    def post(self):
        payload = api.payload
        client_name = payload.get("client_name")
        client_email = payload.get("client_email")
        status_id = payload.get("status_id")
        phone_number = payload.get("phone_number")
        time_period = payload.get("time_period")
        all_booking_ids = payload.get("booking_ids").split(",")
        total_cost = 0.0
        for booking_id in all_booking_ids:
            booking = Booking.query_by_id(booking_id)
            if not booking:
                raise NotFound(f"Item_id {booking_id} no found.")
            diff = booking.end_time - booking.start_time
            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600
            item_price = booking.item.price * hours
            cost = item_price * (100 - booking.discount) / 100
            total_cost += cost
        order = Order(client_name, client_email, phone_number, status_id, time_period, total_cost)
        order.insert()
        for each in all_booking_ids:
            OrderBookings(each, order.id).insert()
        return response_structure(order), 201


@api.route("/<int:order_id>")
class order_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseOrder)
    def get(self, order_id):
        order = Order.query_by_id(order_id)
        return response_structure(order), 200

    @api.doc("Delete item by id")
    def delete(self, order_id):
        Order.delete(order_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseOrder, skip_none=True)
    @api.param("client_name")
    @api.param("client_email")
    @api.param("status_id")
    @api.param("phone_number")
    @api.param("time_period")
    @api.param("booking_ids")
    def patch(self, order_id):
        data = api.payload.copy()

        if "status_id" in data.keys() and int(data["status_id"]) == OrderStatus.get_id_by_name("Completed"):
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
                item_price = float(booking.item.price) * float(hours)
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
        args = api.payload.copy()
        orders_query = Order.getQuery_OrderByItemType(item_type_id)
        allorders, rows = Order.filtration(args, orders_query)
        return response_structure(allorders, rows), 200
