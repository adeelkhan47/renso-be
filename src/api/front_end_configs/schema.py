from flask_restx import fields

from . import api

FrontEndExpect = api.model(
    "Logo_Expect",
    {
        "front_end_configs": fields.String(),
        "front_end_url": fields.String(),
    },
)
FrontEnd = api.model(
    "front_end_configs",
    {
        "id": fields.Integer(),
        "url": fields.String(),
        "front_end_url": fields.String(),

    },
)

get_list_FE_LOGO = api.model(
    "get_list_FE_LOGO",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(FrontEnd, as_list=True),
    },
)
get_by_id_FE_LOGO = api.model(
    "get_by_id_FE_LOGO",
    {
        "objects": fields.Nested(FrontEnd),

    },
)
