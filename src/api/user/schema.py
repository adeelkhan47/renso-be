from flask_restx import fields

from . import api

User = api.model(
    "User",
    {
        "id": fields.Integer(),
        "first_name": fields.String(),
        "last_name": fields.String(),
    },
)

get_list_response = api.model(
    "getAll",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(User, as_list=True),
    },
)
get_by_id_response = api.model(
    "getUserById",
    {
        "objects": fields.Nested(User),

    },
)
