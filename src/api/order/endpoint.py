from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.order import Order
from model.order_bookings import OrderBookings
from . import api, schema


@api.route("")
class order_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_response)
    def get(self):
        args = request.args
        all_items, count = Order.filtration(args)
        return response_structure(all_items, count), 200

    @api.param("client_name", required=True)
    @api.param("client_email", required=True)
    @api.param("phone_number", required=True)
    @api.param("time_period", required=True)
    @api.param("booking_ids", required=True)
    def post(self):
        client_name = request.args.get("client_name")
        client_email = request.args.get("client_email")
        phone_number = request.args.get("phone_number")
        time_period = request.args.get("time_period")
        order = Order(client_name, client_email, phone_number, "Active", time_period)
        order.insert()
        all_booking_ids = request.args.get("booking_ids").split(",")
        for each in all_booking_ids:
            OrderBookings(each, order.id).insert()

        return "ok", 201


@api.route("/<int:order_id>")
class order_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_response)
    def get(self, order_id):
        order = Order.query_by_id(order_id)

        return response_structure(order), 200

    @api.doc("Delete item by id")
    def delete(self, order_id):
        Order.delete(order_id)
        return "ok", 200
