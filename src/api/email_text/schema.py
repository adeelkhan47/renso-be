from flask_restx import fields

from . import api

EmailText_Expect = api.model(
    "ItemTypeText_Expect",
    {
        "text": fields.String(),
    },
)

EmailText = api.model(
    "EmailText",
    {
        "id": fields.Integer(),
        "text": fields.String(),
        "is_deleted": fields.Boolean()

        # "item_type": fields.Nested(Item_type),
    },
)

get_list_EmailText = api.model(
    "getAll_EmailText",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(EmailText, as_list=True),
    },
)
get_by_id_EmailText = api.model(
    "getById_EmailText",
    {
        "objects": fields.Nested(EmailText),

    },
)
