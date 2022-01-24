from datetime import datetime

from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound, BadRequest

from common.helper import response_structure
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
    @api.expect(schema.BookingExpect, validate=True)
    def post(self):
        payload = api.payload
        discount = payload.get("discount")
        location = payload.get("location")
        start_time = payload.get("start_time")
        end_time = payload.get("end_time")
        booking_status_id = payload.get("booking_status_id")
        item_id = payload.get("item_id")
        ##
        item = Item.query_by_id(item_id)
        if not item:
            raise NotFound("Item Not Found.")
        all_bookings = Booking.get_bookings_by_item_id(item.id)
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        day = start_time.strftime('%A')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        for each in all_bookings:
            if each.start_time <= end_time and start_time <= each.end_time:
                raise BadRequest("Item Already booked with this time.")
        booking = Booking(discount, location, start_time, end_time, booking_status_id, item_id)
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
    @api.expect(schema.BookingExpect, validate=True)
    def patch(self, booking_id):
        payload = api.payload
        data = payload.copy()
        Booking.update(booking_id, data)
        booking = Booking.query_by_id(booking_id)
        return response_structure(booking), 200


@api.route("/by_item_type/<int:item_type_id>")
class bookings_by_item_type_id(Resource):
    @api.marshal_list_with(schema.get_list_responseBooking)
    def get(self, item_type_id):
        args = request.args.copy()
        booking_query = Booking.getQuery_BookingByItemType(item_type_id)
        allBookings, rows = Booking.filtration(args, booking_query)
        return response_structure(allBookings, rows), 200


@api.route("/by_item_type/<int:item_subtype_id>")
class bookings_by_item_Subtype_id(Resource):
    @api.marshal_list_with(schema.get_list_responseBooking)
    def get(self, item_subtype_id):
        args = request.args.copy()
        booking_query = Booking.getQuery_BookingByItemSubType(item_subtype_id)
        allBookings, rows = Booking.filtration(args, booking_query)
        return response_structure(allBookings, rows), 200