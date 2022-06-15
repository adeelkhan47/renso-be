from flask_restx import fields

from . import api
from ..item_type.schema import Item_type

ItemTypeText_Expect2 = api.model(
    "ItemTypeText_Expect2",
    {
        "text": fields.String(),
        "item_type_id": fields.Integer(),
    },
)

ItemTypeText = api.model(
    "ItemTypeText",
    {
        "id": fields.Integer(),
        "text": fields.String(),
        "item_type": fields.Nested(Item_type),
    },
)

get_list_ItemTypeText = api.model(
    "getAll_ItemTypeText",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(ItemTypeText, as_list=True),
    },
)
get_by_id_ItemTypeText = api.model(
    "getById_ItemTypeText",
    {
        "objects": fields.Nested(ItemTypeText),

    },
)
