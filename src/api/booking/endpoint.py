from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.booking import Booking
from . import api, schema


@api.route("")
class booking_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_response)
    def get(self):
        args = request.args
        all_items, count = Booking .filtration(args)
        return response_structure(all_items, count), 200

    @api.param("discount", required=True)
    @api.param("location", required=True)
    @api.param("start_time", required=True)
    @api.param("end_time", required=True)
    @api.param("item_id", required=True)
    def post(self):
        discount = request.args.get("discount")
        location = request.args.get("location")
        start_time = request.args.get("start_time")
        end_time = request.args.get("end_time")
        item_id = request.args.get("item_id")

        booking = Booking(discount, location, start_time, end_time, item_id)
        booking.insert()
        return "ok", 201


@api.route("/<int:booking_id>")
class booking_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_response)
    def get(self, booking_id):
        booking = Booking.query_by_id(booking_id)

        return response_structure(booking), 200

    @api.doc("Delete booking by id")
    def delete(self, booking_id):
        Booking.delete(booking_id)
        return "ok", 200
