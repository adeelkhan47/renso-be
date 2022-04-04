from datetime import datetime, timedelta

from flask import request
from flask_restx import Resource
from werkzeug.exceptions import BadRequest, NotFound

from common.helper import response_structure
from model.booking import Booking
from model.booking_status import BookingStatus
from model.cart import Cart
from model.cart_booking import CartBookings
from model.item import Item
from model.item_subtype import ItemSubType
from model.payment_method import PaymentMethod
from model.season import Season
from model.voucher import Voucher
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
        start_time = payload.get("start_time")
        end_time = payload.get("end_time")
        booking_status_id = payload.get("booking_status_id")
        item_id = payload.get("item_id")
        cost = payload.get("cost")
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
        booking = Booking(start_time, end_time, booking_status_id, item_id, cost)
        booking.insert()
        return response_structure(booking), 201


@api.route("/<int:booking_id>")
class booking_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseBooking)
    def get(self, booking_id):
        booking = Booking.query_by_id(booking_id)
        if not booking:
            raise NotFound("Item Not Found.")
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


@api.route("/by_item_subtype/<int:item_subtype_id>")
class bookings_by_item_Subtype_id(Resource):
    @api.marshal_list_with(schema.get_list_responseBooking)
    def get(self, item_subtype_id):
        args = request.args.copy()
        booking_query = Booking.getQuery_BookingByItemSubType(item_subtype_id)
        allBookings, rows = Booking.filtration(args, booking_query)
        return response_structure(allBookings, rows), 200


@api.route("/bulk")
class booking_list(Resource):

    @api.marshal_list_with(schema.get_cart_payments)
    @api.param("cart_id", required=True)
    @api.param("voucher", required=False)
    def get(self):
        args = request.args
        cart = Cart.query_by_id(args.get("cart_id"))
        bookings = [each.booking for each in cart.cart_bookings]
        price_factor = 100
        voucher = None
        if "voucher" in args.keys() and args["voucher"]:
            voucher = Voucher.get_voucher_by_code(args.get("voucher"))
            if voucher:
                price_factor = voucher.price_factor
        payment_method = PaymentMethod.get_payment_method_by_name("Stripe")

        actual_total_price = 0
        effected_total_price = 0
        taxs = []
        for booking in bookings:
            actual_total_price += booking.cost
            effected_total_price += (price_factor / 100) * booking.cost

        tax_amount = 0
        if payment_method:
            for each in payment_method.payment_tax:
                tax = each.tax
                tax_amount += tax.percentage / 100 * effected_total_price
                taxs.append(tax)

        actual_total_price_after_tax = effected_total_price + tax_amount

        response_data = {
            "bookings": bookings,
            "taxs": taxs,
            "actual_total_price": actual_total_price,
            "effected_total_price": effected_total_price,
            "actual_total_price_after_tax": actual_total_price_after_tax,
            "voucher": voucher

        }
        return response_structure(response_data)

    @api.marshal_list_with(schema.get_booking_ids_, skip_none=True)
    @api.expect(schema.bulk_booking_expect, validate=True)
    def post(self):
        payload = api.payload
        start_time = datetime.strptime(payload.get("start_time"), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(payload.get("end_time"), '%Y-%m-%d %H:%M:%S')
        booking_ids = []
        active_status = BookingStatus.get_id_by_name("Active")
        booking_dictionary = {}
        if start_time.date() == end_time.date():
            factor = Season.get_price_factor_on_date(start_time.date())
            for each in payload.get("bookings_details"):
                item_sub_type = ItemSubType.query_by_id(each.get("item_sub_type_id"))
                for item_id in each.get("item_ids"):
                    if (item_sub_type.id, item_id) not in booking_dictionary.keys():
                        booking_dictionary[(item_sub_type.id, item_id)] = 0
                    diff = end_time - start_time
                    days, seconds = diff.days, diff.seconds
                    hours = days * 24 + seconds // 3600
                    booking_dictionary[(item_sub_type.id, item_id)] += (hours * item_sub_type.price) * factor / 100
        else:
            days = (start_time.date() + timedelta(x) for x in range(0, (end_time - start_time).days + 1))
            for day in days:
                factor = Season.get_price_factor_on_date(day)
                for each in payload.get("bookings_details"):
                    item_sub_type = ItemSubType.query_by_id(each.get("item_sub_type_id"))
                    for item_id in each.get("item_ids"):
                        if (item_sub_type.id, item_id) not in booking_dictionary.keys():
                            booking_dictionary[(item_sub_type.id, item_id)] = 0
                        if day == start_time.date():
                            temp_date_time = datetime.combine(day, datetime.max.time())
                            diff = temp_date_time - start_time
                            days, seconds = diff.days, diff.seconds
                            hours = days * 24 + seconds // 3600
                            booking_dictionary[(item_sub_type.id, item_id)] += ((
                                                                                        hours + 1) * item_sub_type.price) * factor / 100
                        elif day == end_time.date():
                            temp_date_time = datetime.combine(day, datetime.min.time())
                            diff = end_time - temp_date_time
                            days, seconds = diff.days, diff.seconds
                            hours = days * 24 + seconds // 3600
                            booking_dictionary[(item_sub_type.id, item_id)] += (
                                                                                       hours * item_sub_type.price) * factor / 100
                        else:
                            booking_dictionary[(item_sub_type.id, item_id)] += (24 * item_sub_type.price) * factor / 100

        for each in payload.get("bookings_details"):
            item_sub_type = each.get("item_sub_type_id")
            for item_id in each.get("item_ids"):
                cost = booking_dictionary[(item_sub_type, item_id)]
                booking = Booking(start_time, end_time, active_status, item_id, cost)
                booking.insert()
                booking_ids.append(booking.id)
        if "cart_id" in payload.keys() and payload.get("cart_id") and Cart.query_by_id(payload.get("cart_id")):
            cart = Cart.query_by_id(payload.get("cart_id"))
        else:
            cart = Cart()
            cart.insert()
        for each in booking_ids:
            CartBookings(cart_id=cart.id, booking_id=each).insert()
        return response_structure({"cart_id": cart.id}), 201
