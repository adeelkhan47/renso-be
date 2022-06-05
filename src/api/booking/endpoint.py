from datetime import datetime, timedelta

from flask import g
from flask import request
from flask_restx import Resource
from werkzeug.exceptions import BadRequest, NotFound

from common.helper import response_structure, error_message
from decorator.authorization import auth
from model.booking import Booking
from model.booking_status import BookingStatus
from model.cart import Cart
from model.cart_booking import CartBookings
from model.front_end_configs import FrontEndCofigs
from model.item import Item
from model.item_subtype import ItemSubType
from model.location import Location
from model.order_backup import OrderBackUp
from model.payment_method import PaymentMethod
from model.season import Season
from model.voucher import Voucher
from . import api, schema


@api.route("")
class booking_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseBooking)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        all_items, count = Booking.filtration(args)
        return response_structure(all_items, count), 200

    @api.marshal_list_with(schema.get_by_id_responseBooking, skip_none=True)
    @api.expect(schema.BookingExpect, validate=True)
    @auth
    def post(self):
        payload = api.payload
        start_time = payload.get("start_time")
        end_time = payload.get("end_time")
        booking_status_id = payload.get("booking_status_id")
        item_id = payload.get("item_id")
        location_id = payload.get("location_id")
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
        booking = Booking(start_time, end_time, booking_status_id, item_id, cost, g.current_user.id, location_id)
        booking.insert()
        return response_structure(booking), 201


@api.route("/<int:booking_id>")
class booking_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseBooking)
    @auth
    def get(self, booking_id):
        booking = Booking.query_by_id(booking_id)
        if not booking:
            raise NotFound("Item Not Found.")
        return response_structure(booking), 200

    @api.doc("Delete booking by id")
    @auth
    def delete(self, booking_id):
        Booking.delete(booking_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseBooking, skip_none=True)
    @api.expect(schema.BookingExpect, validate=True)
    @auth
    def patch(self, booking_id):
        payload = api.payload
        data = payload.copy()
        Booking.update(booking_id, data)
        booking = Booking.query_by_id(booking_id)
        return response_structure(booking), 200


@api.route("/by_item_type/<int:item_type_id>")
class bookings_by_item_type_id(Resource):
    @api.marshal_list_with(schema.get_list_responseBooking)
    @auth
    def get(self, item_type_id):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        booking_query = Booking.getQuery_BookingByItemType(item_type_id)
        allBookings, rows = Booking.filtration(args, booking_query)
        return response_structure(allBookings, rows), 200


@api.route("/by_item_subtype/<int:item_subtype_id>")
class bookings_by_item_Subtype_id(Resource):
    @api.marshal_list_with(schema.get_list_responseBooking)
    @auth
    def get(self, item_subtype_id):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        booking_query = Booking.getQuery_BookingByItemSubType(item_subtype_id)
        allBookings, rows = Booking.filtration(args, booking_query)
        return response_structure(allBookings, rows), 200


@api.route("/bulk")
class booking_list(Resource):

    @api.marshal_list_with(schema.get_cart_payments)
    @api.param("cart_id", required=True)
    @api.param("voucher", required=False)
    @api.param("backup_unique_key", required=False)
    @auth
    def get(self):

        args = request.args
        cart = Cart.query_by_id(args.get("cart_id"))
        edit = False
        order_backup = None
        if "backup_unique_key" in args.keys() and args["backup_unique_key"]:
            order_backup = OrderBackUp.get_order_backUp_by_unique_key(args["backup_unique_key"])
            if order_backup:
                edit = True
            else:
                raise BadRequest("Invalid Request")

        if not cart:
            raise NotFound(error_message("Cart not found."))
        bookings = [each.booking for each in cart.cart_bookings]
        price_factor = 100
        voucher = None
        if not edit:
            if "voucher" in args.keys() and args["voucher"]:
                voucher = Voucher.get_voucher_by_code(args.get("voucher"), g.current_user.id)
                if voucher:
                    price_factor = voucher.price_factor
        else:
            voucher = Voucher.get_voucher_by_code(order_backup.voucher, g.current_user.id)
            if voucher:
                price_factor = voucher.price_factor
        payment_method = PaymentMethod.get_payment_method_by_name("Stripe", g.current_user.id)
        if not payment_method:
            raise NotFound(error_message("Stripe Default Payment not found."))
        actual_total_price = 0
        effected_total_price = 0
        taxs = []
        tax_amount = 0
        for booking in bookings:
            actual_total_price += booking.cost
            temp_tax_amount = 0
            for each in payment_method.payment_tax:
                if booking.item.item_subtype_id in [x.item_sub_type_id for x in each.tax.itemSubTypeTaxs]:
                    temp_tax_amount += (price_factor / 100) * ((each.tax.percentage / 100) * booking.cost)
                    if each.tax not in taxs:
                        taxs.append(each.tax)

            tax_amount += temp_tax_amount
            effected_total_price += (price_factor / 100) * booking.cost

        actual_total_price_after_tax = effected_total_price + tax_amount

        app_configs = FrontEndCofigs.get_by_user_id(g.current_user.id)
        privacy_link = app_configs.privacy_policy_link
        updated_amount = 0
        price_already_paid = 0
        if edit:
            updated_amount = actual_total_price_after_tax - round(float(order_backup.price_paid), 2)
            price_already_paid = round(float(order_backup.price_paid), 2)

        response_data = {
            "bookings": bookings,
            "taxs": taxs,
            "actual_total_price": round(actual_total_price, 2),
            "effected_total_price": round(effected_total_price, 2),
            "actual_total_price_after_tax": round(actual_total_price_after_tax, 2),
            "tax_amount": round(tax_amount, 2),
            "voucher": voucher,
            "privacy_policy_link": privacy_link,
            "isEdited": edit,
            "price_already_paid": round(price_already_paid, 2),
            "updated_amount": round(updated_amount, 2)

        }
        return response_structure(response_data)

    @api.marshal_list_with(schema.get_booking_ids_, skip_none=True)
    @api.expect(schema.bulk_booking_expect, validate=True)
    @auth
    def post(self):
        payload = api.payload
        start_time = datetime.strptime(payload.get("start_time"), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(payload.get("end_time"), '%Y-%m-%d %H:%M:%S')
        location_id = payload.get("location_id")
        location = Location.query_by_id(location_id)

        booking_ids = []
        pending_status = BookingStatus.get_id_by_name("Pending")
        booking_dictionary = {}
        if start_time.date() == end_time.date():
            season_factor = Season.get_price_factor_on_date(start_time.date(), g.current_user.id)
            location_factor = location.price_factor
            factor = 100 + ((season_factor - 100) + (location_factor - 100))

            for each in payload.get("bookings_details"):
                item_sub_type = ItemSubType.query_by_id(each.get("item_sub_type_id"))
                least_price = item_sub_type.least_price
                for item_id in each.get("item_ids"):
                    if (item_sub_type.id, item_id) not in booking_dictionary.keys():
                        booking_dictionary[(item_sub_type.id, item_id)] = 0
                    diff = end_time - start_time
                    days, seconds = diff.days, diff.seconds
                    hours = days * 24 + seconds // 3600
                    price = (hours * item_sub_type.price) * factor / 100
                    final_price = price
                    if least_price > final_price / hours:
                        final_price = least_price * hours
                    booking_dictionary[(item_sub_type.id, item_id)] += final_price
        else:
            days = (start_time.date() + timedelta(x) for x in range(0, (end_time - start_time).days + 1))
            for day_number, day in enumerate(days):
                season_factor = Season.get_price_factor_on_date(day, g.current_user.id)
                location_factor = location.price_factor
                factor = 100 + ((season_factor - 100) + (location_factor - 100))
                for each in payload.get("bookings_details"):
                    item_sub_type = ItemSubType.query_by_id(each.get("item_sub_type_id"))
                    least_price = item_sub_type.least_price
                    discount_after_higher_price = item_sub_type.discount_after_higher_price
                    same_price_days = item_sub_type.same_price_days
                    for item_id in each.get("item_ids"):
                        item = Item.query_by_id(item_id)
                        if (item_sub_type.id, item_id) not in booking_dictionary.keys():
                            booking_dictionary[(item_sub_type.id, item_id)] = 0
                        if day == start_time.date():
                            temp_date_time = datetime.combine(day, datetime.max.time())
                            diff = temp_date_time - start_time
                            days, seconds = diff.days, diff.seconds
                            hours = days * 24 + seconds // 3600
                            price = ((hours + 1) * item_sub_type.price) * factor / 100
                            final_price = price
                            if day_number > same_price_days - 1:
                                internal_factor = (day_number - (same_price_days - 1)) * discount_after_higher_price
                                internal_factor = 100 - internal_factor
                                final_price = final_price * internal_factor / 100
                            if least_price > final_price / (hours + 1):
                                final_price = least_price * (hours + 1)
                            booking_dictionary[(item_sub_type.id, item_id)] += final_price
                        elif day == end_time.date():
                            temp_date_time = datetime.combine(day, datetime.min.time())
                            diff = end_time - temp_date_time
                            days, seconds = diff.days, diff.seconds
                            if item.item_type.show_time_picker == False:
                                hours = 24
                            else:
                                hours = days * 24 + seconds // 3600

                            price = (hours * item_sub_type.price) * factor / 100
                            final_price = price
                            if day_number > same_price_days - 1:
                                internal_factor = (day_number - (same_price_days - 1)) * discount_after_higher_price
                                internal_factor = 100 - internal_factor
                                final_price = final_price * internal_factor / 100
                            if least_price > final_price / hours:
                                final_price = least_price * hours
                            booking_dictionary[(item_sub_type.id, item_id)] += final_price

                        else:
                            price = (24 * item_sub_type.price) * factor / 100
                            final_price = price
                            if day_number > same_price_days - 1:
                                internal_factor = (day_number - (same_price_days - 1)) * discount_after_higher_price
                                internal_factor = 100 - internal_factor
                                final_price = final_price * internal_factor / 100
                            if least_price > final_price / 24:
                                final_price = least_price * 24
                            booking_dictionary[(item_sub_type.id, item_id)] += final_price

        for each in payload.get("bookings_details"):
            item_sub_type = each.get("item_sub_type_id")
            for item_id in each.get("item_ids"):
                cost = booking_dictionary[(item_sub_type, item_id)]
                self.booking = Booking(start_time, end_time, pending_status, item_id, round(cost, 2), g.current_user.id,
                                       location.id)
                booking = self.booking
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
