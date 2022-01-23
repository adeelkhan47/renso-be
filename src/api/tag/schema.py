from flask_restx import fields

from . import api

Tag_Expect = api.model(
    "Tag_Expect",
    {
        "name": fields.String(),
        "description": fields.String(),
        "color": fields.String(),

    },
)

Tag = api.model(
    "tag",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "description": fields.String(),
        "color": fields.String(),

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
