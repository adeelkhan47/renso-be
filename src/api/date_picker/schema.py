from flask_restx import fields

from . import api

Date_Picker = api.model(
    "booking",
    {
        "id": fields.Integer(),
        "allowed_days": fields.String(),
        "not_allowed_days": fields.String(),

    },
)

get_list_response = api.model(
    "getAll",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Date_Picker, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById",
    {
        "objects": fields.Nested(Date_Picker),

    },
)
