from flask_restx import fields

from . import api
# from ..item_subtype.schema import Item_subtype
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
Item_type_extra_Expect = api.model(
    "Item_type_extra_Expect",
    {
        "item_type_id": fields.String(),
        "item_sub_type_ids": fields.String()
    },
)

Item_subtype_temp = api.model(
    "Item_subtype_temp",
    {
        "id": fields.Integer(),
        "price": fields.Float(),
        "name": fields.String(),
        "image": fields.String(),
        "person": fields.Integer()

    },
)
locations = api.model(
    "locations",
    {"location": fields.Nested(Location, as_list=True)}
)
item_sub_types = api.model(
    "item_sub_types_for_extra",
    {"item_subtype": fields.Nested(Item_subtype_temp, as_list=True)}
)

Item_type = api.model(
    "item_type_1",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "maintenance": fields.Integer(),
        "delivery_available": fields.Boolean(),
        "show_time_picker": fields.Boolean(),
        "image": fields.String(),
        "itemTypeLocations": fields.Nested(locations, as_list=True),
        "itemTypeExtras": fields.Nested(item_sub_types, as_list=True),
        "item_sub_type": fields.Nested(Item_subtype_temp, as_list=True)
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
