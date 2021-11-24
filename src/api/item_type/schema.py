from flask_restx import fields

from . import api
from ..item.schema import Item

Item_type = api.model(
    "User",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "maintenance": fields.Integer(),
        "delivery_available": fields.String(),
        "items": fields.Nested(Item)

    },
)

get_list_response = api.model(
    "getAll",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Item_type, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById",
    {
        "objects": fields.Nested(Item_type),

    },
)
