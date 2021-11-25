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

    @api.param("name", required=True)
    def post(self):
        name = request.args.get("name")

        widget = BookingWidget(name, "Active")
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
