from flask_restx import fields

from . import api
from ..booking.schema import Booking

bookings = api.model(
    "bookings",
    {"booking": fields.Nested(Booking, as_list=True)}
)
Order = api.model(
    "Order",
    {
        "id": fields.Integer(),
        "client_name": fields.String(),
        "client_email": fields.String(),
        "phone_number": fields.String(),
        "status": fields.String(),
        "time_period": fields.String(),
        "order_bookings": fields.Nested(bookings, as_list=True)
    },
)

get_list_response = api.model(
    "getAll_Order",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Order, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById_Order",
    {
        "objects": fields.Nested(Order),

    },
)
