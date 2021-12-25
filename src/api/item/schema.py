from flask_restx import fields

from . import api
from ..tag.schema import Tag
from ..user.schema import User
from ..item_type.schema import Item_type

tags = api.model(
    "tags",
    {"tag": fields.Nested(Tag, as_list=True)}
)
Item = api.model(
    "item",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "image": fields.String(),
        "description": fields.String(),
        "price": fields.Integer(),
        "item_type": fields.Nested(Item_type),
        "item_tags": fields.Nested(tags, as_list=True)
    },
)

get_list_responseItem = api.model(
    "getAll_item",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Item, as_list=True),
    },
)
get_by_id_responseItem = api.model(
    "getById_item",
    {
        "objects": fields.Nested(Item),

    },
)
