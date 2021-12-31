from datetime import datetime

from flask import request
from flask_restx import Resource

from common.helper import response_structure, error_message
from model.booking import Booking
from model.item import Item
from . import api, schema


@api.route("")
class booking_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseBooking)
    def get(self):
        args = request.args
        all_items, count = Booking.filtration(args)
        return response_structure(all_items, count), 200

    @api.marshal_list_with(schema.get_by_id_responseBooking, skip_none=True)
    @api.param("discount", required=True)
    @api.param("location", required=True)
    @api.param("start_time", required=True)
    @api.param("end_time", required=True)
    @api.param("status", required=True)
    @api.param("item_id", required=True, type=int)
    def post(self):
        discount = request.args.get("discount")
        location = request.args.get("location")
        start_time = request.args.get("start_time")
        end_time = request.args.get("end_time")
        status = request.args.get("status")
        item_id = request.args.get("item_id")
        ##
        item = Item.query_by_id(item_id)
        if not item:
            return error_message("Item Not Found."), 404
        all_bookings = Booking.get_bookings_by_item_id(item.id)
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        day = start_time.strftime('%A')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        for each in all_bookings:
            if each.start_time <= end_time and start_time <= each.end_time:
                return error_message("Item Already booked with this time."), 400
        booking = Booking(discount, location, start_time, end_time, status, item_id)
        booking.insert()
        return response_structure(booking), 201


@api.route("/<int:booking_id>")
class booking_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseBooking)
    def get(self, booking_id):
        booking = Booking.query_by_id(booking_id)

        return response_structure(booking), 200

    @api.doc("Delete booking by id")
    def delete(self, booking_id):
        Booking.delete(booking_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseBooking, skip_none=True)
    @api.param("discount")
    @api.param("location")
    @api.param("start_time")
    @api.param("end_time")
    @api.param("status")
    @api.param("item_id")
    def patch(self, booking_id):
        data = request.args.copy()
        Booking.update(booking_id, data)
        booking = Booking.query_by_id(booking_id)
        return response_structure(booking), 200
