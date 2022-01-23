from flask_restx import fields

from . import api

LanguageExpect = api.model(
    "languageLanguageExpect",
    {
        "name": fields.String(),
        "status": fields.Boolean(),

    },
)
Language = api.model(
    "language",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "status": fields.Boolean(),

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
