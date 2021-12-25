from flask_restx import fields

from . import api

Item_type = api.model(
    "item_type",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "maintenance": fields.Integer(),
        "delivery_available": fields.String(),
        #"items": fields.Nested(Item)

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
