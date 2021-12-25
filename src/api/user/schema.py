from flask_restx import fields

from . import api

User = api.model(
    "User",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "email": fields.String(),
        "subscription": fields.String(),
        "status": fields.String(),

    },
)

get_list_responseUser = api.model(
    "getAll_User",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(User, as_list=True),
    },
)
get_by_id_responseUser = api.model(
    "getUserById_User",
    {
        "objects": fields.Nested(User),

    },
)
