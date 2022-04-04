from flask_restx import fields

from ..item_status.schema import ItemStatus
from ..item_subtype.schema import Item_subtype
from ..item_type.schema import Item_type
from ..location.schema import Location
from ..tag.schema import Tag
from . import api

ItemExpect = api.model(
    "itemExpect",
    {
        "name": fields.String(),
        "image": fields.String(),
        "image_key": fields.String(),
        "description": fields.String(),
        "item_type_id": fields.Integer(),
        "item_subtype_id": fields.Integer(),
        "tag_ids": fields.String(),
        "location_ids": fields.String()
    },
)

tags = api.model(
    "tags",
    {"tag": fields.Nested(Tag, as_list=True)}
)

locations = api.model(
    "locations",
    {"location": fields.Nested(Location, as_list=True)}
)

Item = api.model(
    "item",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "image": fields.String(),
        "image_key": fields.String(),
        "description": fields.String(),
        "item_status": fields.Nested(ItemStatus),
        "item_type": fields.Nested(Item_type),
        "item_subtype": fields.Nested(Item_subtype),
        "item_tags": fields.Nested(tags, as_list=True),
        "item_locations": fields.Nested(locations, as_list=True),
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
