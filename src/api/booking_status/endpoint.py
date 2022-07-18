from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.booking_status import BookingStatus

from . import api, schema


@api.route("")
class BookingStatusList(Resource):
    @api.doc("Get all BookingStatus")
    @api.marshal_list_with(schema.get_list_responseBookingStatus)
    def get(self):
        args = request.args
        args["is_deleted:eq"] = "False"
        all_rows, count = BookingStatus.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.BookingStatusExpect)
    @api.marshal_list_with(schema.get_by_id_responseBookingStatus)
    def post(self):
        payload = api.payload
        name = payload.get("name")
        color = payload.get("color")
        order_status = BookingStatus(name, color)
        order_status.insert()

        return response_structure(order_status), 201


@api.route("/<int:booking_status_id>")
class BookingStatus_by_id(Resource):
    @api.doc("Get booking_status by id")
    @api.marshal_list_with(schema.get_by_id_responseBookingStatus)
    def get(self, booking_status_id):
        bookingStatus = BookingStatus.query_by_id(booking_status_id)
        return response_structure(bookingStatus), 200

    @api.doc("Delete method by id")
    def delete(self, booking_status_id):
        BookingStatus.soft_delete(booking_status_id)
        return "ok", 200
