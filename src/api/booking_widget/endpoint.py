from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.booking_widget import BookingWidget

from . import api, schema


@api.route("")
class BookingWidgetList(Resource):
    @api.doc("Get all Booking Widgets")
    @api.marshal_list_with(schema.get_list_responseBooking_Widget)
    def get(self):
        args = request.args
        all_rows, count = BookingWidget.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.Booking_Widget_Expect)
    @api.marshal_list_with(schema.get_by_id_responseBooking_Widget)
    def post(self):
        payload = api.payload
        # time_picker_status = int(payload.get("time_picker"))
        # day_picker_status = int(payload.get("day_picker_status"))
        # date_range_Picker_status = int(payload.get("date_range_Picker_status"))
        widget = BookingWidget(**payload)
        widget.insert()
        return response_structure(widget), 201


@api.route("/<int:booking_widget_id>")
class widget_by_id(Resource):
    @api.doc("Get Widget by id")
    @api.marshal_list_with(schema.get_by_id_responseBooking_Widget)
    def get(self, booking_widget_id):
        widget = BookingWidget.query_by_id(booking_widget_id)
        return response_structure(widget), 200

    @api.doc("Delete Widget by id")
    def delete(self, booking_widget_id):
        BookingWidget.delete(booking_widget_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseBooking_Widget, skip_none=True)
    @api.expect(schema.Booking_Widget_Expect)
    def patch(self, booking_widget_id):
        # data = {}
        payload = api.payload
        # data["time_picker_status"] = payload.get("time_picker_status"))
        # data["day_picker_status"] = payload.get("day_picker_status")
        # data["date_range_picker_status"] = int(payload.get("date_range_picker_status"))
        BookingWidget.update(booking_widget_id, **payload)
        bookingWidget = BookingWidget.query_by_id(booking_widget_id)
        return response_structure(bookingWidget), 200
