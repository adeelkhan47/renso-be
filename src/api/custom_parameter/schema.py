from flask_restx import fields

from . import api

CustomParameterExpect = api.model(
    "CustomParameterExpect",
    {
        "name": fields.String(),

    },
)

CustomParameter = api.model(
    "customParameter",
    {
        "id": fields.Integer(),
        "name": fields.String(),
    },
)

get_list_CustomParameter = api.model(
    "getAll_CustomParameter",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(CustomParameter, as_list=True),
    },
)
get_by_id_CustomParameter = api.model(
    "getById_CustomParameter",
    {
        "objects": fields.Nested(CustomParameter),

    },
)
