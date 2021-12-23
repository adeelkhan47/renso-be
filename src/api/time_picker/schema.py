from flask_restx import fields

from . import api
from ..day_picker.schema import Day_Picker

Time_Picker = api.model(
    "booking",
    {
        "id": fields.Integer(),
        "start_time": fields.String(),
        "end_time": fields.String(),
        "day": fields.String(),
        #"day_picker": fields.Nested(Day_Picker),

    },
)

get_list_response = api.model(
    "getAll_booking",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Time_Picker, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById_booking",
    {
        "objects": fields.Nested(Time_Picker),

    },
)
