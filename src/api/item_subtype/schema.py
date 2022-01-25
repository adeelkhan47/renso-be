from flask_restx import fields

from . import api
from ..item_type.schema import Item_type

Item_subtype_Expect = api.model(
    "item_type_expect",
    {

        "name": fields.String(),
        "price": fields.Integer(),
        "person": fields.Integer(),
        "item_type_id": fields.Integer(),
    },
)

Item_subtype = api.model(
    "item_type",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "person": fields.Integer(),
        "item_type": fields.Nested(Item_type),

    },
)

get_list_responseItem_Subtype = api.model(
    "getAll_item_type",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Item_subtype, as_list=True),
    },
)
get_by_id_responseItem_Subtype = api.model(
    "getById_item_type",
    {
        "objects": fields.Nested(Item_subtype),

    },
)
