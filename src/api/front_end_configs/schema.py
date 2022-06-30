from flask_restx import fields

from . import api

FrontEndExpect = api.model(
    "Logo_Expect",
    {
        "logo": fields.String(),
        "front_end_url": fields.String(),
        "email": fields.String(),
        "email_password": fields.String(),
        "link1": fields.String(),
        "link2": fields.String(),
        "link1_name": fields.String(),
        "link2_name": fields.String(),
    },
)
FrontEnd = api.model(
    "front_end_configs",
    {
        "id": fields.Integer(),
        "logo": fields.String(),
        "front_end_url": fields.String(),
        "email": fields.String(),
        "email_password": fields.String(),
        "link1": fields.String(),
        "link2": fields.String(),
        "link1_name": fields.String(),
        "link2_name": fields.String(),
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
