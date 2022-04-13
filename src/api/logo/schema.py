from flask_restx import fields

from . import api

Logo_Expect = api.model(
    "Logo_Expect",
    {
        "url": fields.String(),
    },
)
Logo = api.model(
    "logo",
    {
        "id": fields.Integer(),
        "url": fields.String()

    },
)

get_list_FE_LOGO = api.model(
    "get_list_FE_LOGO",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Logo, as_list=True),
    },
)
get_by_id_FE_LOGO = api.model(
    "get_by_id_FE_LOGO",
    {
        "objects": fields.Nested(Logo),

    },
)
