from flask_restx import fields

from . import api
from ..item_type.schema import Item_type

Item_subtype_Expect = api.model(
    "item_subtype_expect",
    {

        "name": fields.String(),
        "price": fields.Float(),
        "person": fields.Integer(),
        "item_type_id": fields.Integer(),
        "image": fields.String(),
        "least_price": fields.Float(),
        "discount_after_higher_price": fields.Integer(),
        "same_price_days": fields.Integer()
    },
)

Item_subtype = api.model(
    "item_sub_type",
    {
        "id": fields.Integer(),
        "price": fields.Float(),
        "name": fields.String(),
        "image": fields.String(),
        "person": fields.Integer(),
        "item_type": fields.Nested(Item_type),
        "least_price": fields.Float(),
        "discount_after_higher_price": fields.Integer(),
        "same_price_days": fields.Integer()

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
