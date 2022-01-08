from flask_restx import fields

from . import api

BookingStatus = api.model(
    "bookingStatus",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "color": fields.String(),

    },
)

get_list_responseBookingStatus = api.model(
    "getAll_Tag",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(BookingStatus, as_list=True),
    },
)
get_by_id_responseBookingStatus = api.model(
    "getById_tag",
    {
        "objects": fields.Nested(BookingStatus),

    },
)
