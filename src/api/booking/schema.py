from flask_restx import fields

from . import api
from ..booking_status.schema import BookingStatus
from ..item.schema import Item

BookingExpect = api.model(
    "BookingExpect",
    {
        "discount": fields.Integer(),
        "location": fields.String(),
        "start_time": fields.DateTime(),
        "end_time": fields.DateTime(),
        "booking_status_id": fields.Integer(),
        "item_id": fields.Integer(),
    },
)

Booking = api.model(
    "booking",
    {
        "id": fields.Integer(),
        "discount": fields.Integer(),
        "location": fields.String(),
        "start_time": fields.DateTime(),
        "end_time": fields.DateTime(),
        "booking_status": fields.Nested(BookingStatus),
        "item": fields.Nested(Item),

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
