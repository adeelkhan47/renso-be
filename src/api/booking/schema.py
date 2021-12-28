from flask_restx import fields

from . import api
from ..item.schema import Item

Booking = api.model(
    "booking",
    {
        "id": fields.Integer(),
        "discount": fields.Integer(),
        "location": fields.String(),
        "start_time": fields.DateTime(),
        "end_time": fields.DateTime(),
        "status": fields.String(),
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