from flask_restx import fields

from . import api

AssociateEmail_Expect = api.model(
    "AssociateEmail_Expect",
    {
        "email": fields.String(),
        "status": fields.Boolean(),
    },
)

AssociateEmail = api.model(
    "associateEmail",
    {
        "id": fields.Integer(),
        "email": fields.String(),
        "status": fields.Boolean(),
    },
)

get_list_responseAssociateEmail = api.model(
    "getAll_AssociateEmail",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(AssociateEmail, as_list=True),
    },
)
get_by_id_responseAssociateEmail = api.model(
    "getById_AssociateEmail",
    {
        "objects": fields.Nested(AssociateEmail),

    },
)
