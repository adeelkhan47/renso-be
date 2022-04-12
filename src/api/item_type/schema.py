from flask_restx import fields

from . import api
from ..location.schema import Location

Item_type_Expect = api.model(
    "item_type_expect",
    {

        "name": fields.String(),
        "maintenance": fields.Integer(),
        "delivery_available": fields.Boolean(),
        "image": fields.String(),
        "location_ids": fields.String()
    },
)
locations = api.model(
    "locations",
    {"location": fields.Nested(Location, as_list=True)}
)

Item_type = api.model(
    "item_type_1",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "maintenance": fields.Integer(),
        "delivery_available": fields.Boolean(),
        "image": fields.String(),
        "itemTypeLocations": fields.Nested(locations, as_list=True),
        # "items": fields.Nested(Item)

    },
)

get_list_responseItem_type = api.model(
    "getAll_item_type",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Item_type, as_list=True),
    },
)
get_by_id_responseItem_type = api.model(
    "getById_item_type",
    {
        "objects": fields.Nested(Item_type),

    },
)
