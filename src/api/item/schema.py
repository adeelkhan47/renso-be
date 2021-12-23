from flask_restx import fields

from . import api
from ..user.schema import User
from ..item_type.schema import Item_type

Item = api.model(
    "item",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "image": fields.String(),
        "tags": fields.String(),
        "description": fields.String(),
        "price": fields.Integer(),
        "user":  fields.Nested(User),
        "item_type": fields.Nested(Item_type)
    },
)

get_list_response = api.model(
    "getAll_item",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Item, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById_item",
    {
        "objects": fields.Nested(Item),

    },
)
