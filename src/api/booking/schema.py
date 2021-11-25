from flask_restx import fields

from . import api
from ..item.schema import Item

Booking = api.model(
    "booking",
    {
        "id": fields.Integer(),
        "discount": fields.Integer(),
        "location": fields.String(),
        "start_time": fields.String(),
        "end_time": fields.String(),
        "item": fields.Nested(Item),

    },
)


get_list_response = api.model(
    "getAll",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Booking, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById",
    {
        "objects": fields.Nested(Booking),

    },
)
