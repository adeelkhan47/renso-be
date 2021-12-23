from flask_restx import fields

from . import api
from ..item_type.schema import Item_type

Day_Picker = api.model(
    "booking",
    {
        "id": fields.Integer(),
        "monday": fields.Boolean(),
        "tuesday": fields.Boolean(),
        "wednesday": fields.Boolean(),
        "thursday": fields.Boolean(),
        "friday": fields.Boolean(),
        "saturday": fields.Boolean(),
        "sunday": fields.Boolean(),
        "item_type": fields.Nested(Item_type),

    },
)

get_list_response = api.model(
    "getAll_booking",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Day_Picker, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById_booking",
    {
        "objects": fields.Nested(Day_Picker),

    },
)
