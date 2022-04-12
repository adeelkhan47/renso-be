from flask import g
from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.booking_widget import BookingWidget
from . import api, schema


@api.route("")
class BookingWidgetList(Resource):
    @api.doc("Get all Booking Widgets")
    @api.marshal_list_with(schema.get_list_responseBooking_Widget)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        all_rows, count = BookingWidget.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.Booking_Widget_Expect)
    @api.marshal_list_with(schema.get_by_id_responseBooking_Widget)
    @auth
    def post(self):
        payload = api.payload.copy()
        payload["user_id"] = g.current_user.id
        widget = BookingWidget(**payload)
        widget.insert()
        return response_structure(widget), 201


@api.route("/<int:booking_widget_id>")
class widget_by_id(Resource):
    @api.doc("Get Widget by id")
    @api.marshal_list_with(schema.get_by_id_responseBooking_Widget)
    @auth
    def get(self, booking_widget_id):
        widget = BookingWidget.query_by_id(booking_widget_id)
        return response_structure(widget), 200

    @api.doc("Delete Widget by id")
    @auth
    def delete(self, booking_widget_id):
        BookingWidget.delete(booking_widget_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseBooking_Widget, skip_none=True)
    @api.expect(schema.Booking_Widget_Expect)
    @auth
    def patch(self, booking_widget_id):
        payload = api.payload
        BookingWidget.update(booking_widget_id, **payload)
        bookingWidget = BookingWidget.query_by_id(booking_widget_id)
        return response_structure(bookingWidget), 200
