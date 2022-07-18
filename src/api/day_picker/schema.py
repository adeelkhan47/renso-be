from flask_restx import fields

from ..item_subtype.schema import Item_subtype
from ..item_type.schema import Item_type
from . import api

Day_Picker_Expect = api.model(
    "day_picker_Expect",
    {
        "monday": fields.Boolean(),
        "tuesday": fields.Boolean(),
        "wednesday": fields.Boolean(),
        "thursday": fields.Boolean(),
        "friday": fields.Boolean(),
        "saturday": fields.Boolean(),
        "sunday": fields.Boolean(),
        "item_type_id": fields.Integer(),
    },
)
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
        "is_deleted": fields.Boolean()

    },
)

get_list_responseDay_Picker = api.model(
    "getAll_booking",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Day_Picker, as_list=True),
    },
)
get_by_id_responseDay_Picker = api.model(
    "getById_booking",
    {
        "objects": fields.Nested(Day_Picker),

    },
)
