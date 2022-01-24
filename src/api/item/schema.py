from flask_restx import fields

from . import api
from ..item_status.schema import ItemStatus
from ..item_type.schema import Item_type
from ..tag.schema import Tag

ItemExpect = api.model(
    "item",
    {
        "name": fields.String(),
        "image": fields.String(),
        "description": fields.String(),
        "item_status_id": fields.Integer(),
        "item_type_id": fields.Integer(),
        "item_subtype_id": fields.Integer(),
        "tag_ids": fields.String()
    },
)

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
        "item_status": fields.Nested(ItemStatus),
        "person": fields.String(),
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
