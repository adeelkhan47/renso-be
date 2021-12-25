from flask_restx import fields

from . import api

Tag = api.model(
    "tag",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "description": fields.String(),
    },
)

get_list_responseTag = api.model(
    "getAll_Tag",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Tag, as_list=True),
    },
)
get_by_id_responseTag = api.model(
    "getById_tag",
    {
        "objects": fields.Nested(Tag),

    },
)
