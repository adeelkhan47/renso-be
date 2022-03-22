from flask_restx import fields

from ..item_type.schema import Item_type
from . import api

Item_subtype_Expect = api.model(
    "item_subtype_expect",
    {

        "name": fields.String(),
        "price": fields.Integer(),
        "person": fields.Integer(),
        "item_type_id": fields.Integer(),
    },
)

Item_subtype = api.model(
    "item_sub_type",
    {
        "id": fields.Integer(),
        "price": fields.Integer(),
        "name": fields.String(),
        "person": fields.Integer(),
        "item_type": fields.Nested(Item_type),

    },
)

Availability_Response = api.model(
    "availability_response",
    {
        "item_sub_type_object": fields.Nested(Item_subtype),
        "available_item_ids": fields.List(fields.Integer()),
    }

)

get_list_responseItem_Subtype = api.model(
    "getAll_item_type",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Item_subtype, as_list=True),
    },
)

get_list_Availability_responseItem_Subtype_ = api.model(
    "getAll_Availability_item_type",
    {
        "total_rows": fields.Integer(),
        "objects": fields.List(fields.Nested(Availability_Response, as_list=True)),
    },
)
get_by_id_responseItem_Subtype = api.model(
    "getById_item_type",
    {
        "objects": fields.Nested(Item_subtype),

    },
)
