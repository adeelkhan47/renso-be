from flask_restx import fields

from . import api

Booking_Widget_Expect = api.model(
    "Booking_widget_expect",
    {
        "day_picker_status": fields.Boolean(),
        "time_picker_status": fields.Boolean(),
        "date_range_picker_status": fields.Boolean(),
    },
)
Booking_Widget = api.model(
    "Booking_widget",
    {
        "id": fields.Integer(),

        "day_picker_status": fields.Boolean(),
        "time_picker_status": fields.Boolean(),
        "date_range_picker_status": fields.Boolean(),

    },
)

get_list_responseBooking_Widget = api.model(
    "getAll_Booking_widget",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Booking_Widget, as_list=True),
    },
)
get_by_id_responseBooking_Widget = api.model(
    "getById_Booking_widget",
    {
        "objects": fields.Nested(Booking_Widget),

    },
)
