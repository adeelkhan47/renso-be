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

get_list_responseLanguage = api.model(
    "getAll_language",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Language, as_list=True),
    },
)
get_by_id_responseLanguage = api.model(
    "getById_language",
    {
        "objects": fields.Nested(Language),

    },
)
