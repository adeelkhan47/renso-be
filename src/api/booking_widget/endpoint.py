from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.booking_widget import BookingWidget
from . import api, schema


@api.route("")
class BookingWidgetList(Resource):
    @api.doc("Get all Booking Widgets")
    @api.marshal_list_with(schema.get_list_response)
    def get(self):
        args = request.args
        all_rows, count = BookingWidget.filtration(args)
        return response_structure(all_rows, count), 200

    @api.param("time_picker", required=True, type=int)
    @api.param("date_picker", required=True, type=int)
    @api.param("date_range_Picker", required=True, type=int)
    def post(self):
        time_picker = bool(request.args.get("time_picker"))
        date_picker = bool(request.args.get("date_picker"))
        date_range_Picker = bool(request.args.get("date_range_Picker"))
        widget = BookingWidget(date_picker=date_picker, time_Picker=time_picker, date_range_Picker=date_range_Picker)
        widget.insert()
        return "ok", 201


@api.route("/<int:booking_widget_id>")
class widget_by_id(Resource):
    @api.doc("Get Widget by id")
    @api.marshal_list_with(schema.get_by_id_response)
    def get(self, booking_widget_id):
        widget = BookingWidget.query_by_id(booking_widget_id)
        return response_structure(widget), 200

    @api.doc("Delete Widget by id")
    def delete(self, booking_widget_id):
        BookingWidget.delete(booking_widget_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_response, skip_none=True)
    @api.param("time_picker", required=True, type=int)
    @api.param("date_picker", required=True, type=int)
    @api.param("date_range_Picker", required=True, type=int)
    def patch(self, booking_widget_id):
        data = {}
        data["time_picker"] = bool(request.args.get("time_picker"))
        data["date_picker"] = bool(request.args.get("date_picker"))
        data["date_range_Picker"] = bool(request.args.get("date_range_Picker"))
        BookingWidget.update(booking_widget_id, data)
        bookingWidget = BookingWidget.query_by_id(booking_widget_id)
        return response_structure(bookingWidget), 200
