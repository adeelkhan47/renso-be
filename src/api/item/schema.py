from flask_restx import fields

from . import api
from ..user.schema import User

Item = api.model(
    "User",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "image": fields.String(),
        "tags": fields.String(),
        "description": fields.String(),
        "price": fields.Integer(),
        "user":  fields.Nested(User),
    },
)

get_list_response = api.model(
    "getAll",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Item, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById",
    {
        "objects": fields.Nested(Item),

    },
)
