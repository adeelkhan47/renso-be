from flask_restx import fields

from . import api

Booking_Widget = api.model(
    "Booking_widget",
    {
        "id": fields.Integer(),

        "date_picker": fields.Boolean(),
        "time_picker": fields.Boolean(),
        "date_range_picker": fields.Boolean(),

    },
)

get_list_response = api.model(
    "getAll_Booking_widget",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Booking_Widget, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById_Booking_widget",
    {
        "objects": fields.Nested(Booking_Widget),

    },
)
