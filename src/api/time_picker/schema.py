from flask_restx import fields

from . import api

Time_Picker_expect = api.model(
    "time_Picker_expect",
    {

        "start_time": fields.String(),
        "end_time": fields.String(),
        "day": fields.String(),
        "day_picker_id": fields.Integer(),

    },
)
Time_Picker = api.model(
    "booking",
    {
        "id": fields.Integer(),
        "start_time": fields.String(),
        "end_time": fields.String(),
        "day": fields.String(),
        "day_picker_id": fields.Integer(),

    },
)

get_list_responseTime_Picker = api.model(
    "getAll_booking",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Time_Picker, as_list=True),
    },
)
get_by_id_responseTime_Picker = api.model(
    "getById_booking",
    {
        "objects": fields.Nested(Time_Picker),

    },
)
