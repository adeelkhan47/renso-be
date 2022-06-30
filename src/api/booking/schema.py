from flask_restx import fields

from . import api
from ..booking_status.schema import BookingStatus
from ..item.schema import Item
from ..location.schema import Location
from ..voucher.schema import Voucher

booking_count_ = api.model(
    "booking_count_",
    {
        "item_sub_type_id": fields.Integer(),
        "item_ids": fields.List(fields.Integer()),
    },
)
tax_obj = api.model(
    "tax_obj",
    {
        "tax_name": fields.String(),
        "tax_amount": fields.String(),
    },
)

bulk_booking_expect = api.model(
    "bulk_booking_expect",
    {
        "start_time": fields.String(),
        "end_time": fields.String(),
        "bookings_details": fields.List(fields.Nested(booking_count_)),
        "cart_id": fields.Integer(),
        "location_id": fields.Integer(),

    }
)

BookingExpect = api.model(
    "BookingExpect",
    {
        "discount": fields.Integer(),
        "start_time": fields.DateTime(),
        "end_time": fields.DateTime(),
        "booking_status_id": fields.Integer(),
        "item_id": fields.Integer(),
        "location_id": fields.Integer(),
        "cost": fields.Float(),
        "cost_without_tax": fields.Float(),

    },
)

DummyOrder = api.model(
    "dummyorder",
    {
        "id": fields.Integer()
    }
)
order_bookings = api.model(
    "order_bookings",
    {"order_id": fields.Integer()}
)

Booking = api.model(
    "booking",
    {
        "id": fields.Integer(),
        "cost": fields.Float(),
        "cost_without_tax": fields.Float(),
        "start_time": fields.DateTime(),
        "end_time": fields.DateTime(),
        "booking_status": fields.Nested(BookingStatus),
        "item": fields.Nested(Item),
        "location": fields.Nested(Location),
        "order_bookings": fields.Nested(order_bookings, as_list=True)

    },
)

Cart = api.model(
    "cart",
    {
        "bookings": fields.Nested(Booking, skip_none=True, as_list=True),
        "taxs": fields.List(fields.Nested(tax_obj, as_list=True)),
        "price": fields.Float(),
        "final_price": fields.Float(),
        "voucher": fields.Nested(Voucher, skip_none=True),
        "isEdited": fields.Boolean(),
        "price_already_paid": fields.Float(),
        "updated_amount": fields.Float(),
    },
)
error = api.model(
    "Error",
    {

        "msg": fields.String(),

    },
)

get_list_responseBooking = api.model(
    "getAll",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Booking, as_list=True, skip_none=True, allow_null=True),
        "error": fields.Nested(error, allow_null=True),
    },
)
get_by_id_responseBooking = api.model(
    "getById",
    {
        "objects": fields.Nested(Booking, skip_none=True, allow_null=True),
        "error": fields.Nested(error, allow_null=True),

    },
)
get_cart_payments = api.model(
    "get_cart_payments",
    {
        "objects": fields.Nested(Cart, skip_none=True, allow_null=True),
        "error": fields.Nested(error, allow_null=True),

    },
)

cart_id = api.model(
    "cart_id",
    {
        "cart_id": fields.Integer()
    }
)

get_booking_ids_ = api.model(
    "get_booking_ids_",
    {
        "objects": fields.Nested(cart_id, skip_none=True, allow_null=True),
        "error": fields.Nested(error, allow_null=True),

    },
)
