from flask_restx import fields

from . import api

ItemStatus_Expect = api.model(
    "itemStatusExpect",
    {

        "name": fields.String(),
        "color": fields.String(),

    },
)
ItemStatus = api.model(
    "itemStatus",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "color": fields.String(),
        "is_deleted": fields.Boolean()

    },
)

get_list_responseItemStatus = api.model(
    "getAll_Tag",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(ItemStatus, as_list=True),
    },
)
get_by_id_responseItemStatus = api.model(
    "getById_tag",
    {
        "objects": fields.Nested(ItemStatus),

    },
)
