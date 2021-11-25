from flask_restx import fields

from . import api

Language = api.model(
    "language",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "status": fields.String(),

    },
)

get_list_response = api.model(
    "getAll",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Language, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById",
    {
        "objects": fields.Nested(Language),

    },
)
