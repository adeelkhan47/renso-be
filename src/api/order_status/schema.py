from flask_restx import fields

from . import api

OrderStatus = api.model(
    "orderStatus",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "color": fields.String(),

    },
)

get_list_responseOrderStatus = api.model(
    "getAll_Tag",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(OrderStatus, as_list=True),
    },
)
get_by_id_responseOrderStatus = api.model(
    "getById_tag",
    {
        "objects": fields.Nested(OrderStatus),

    },
)
