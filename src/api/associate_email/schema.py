from flask_restx import fields

from . import api
from ..item_subtype.schema import Item_subtype

AssociateEmail_Expect = api.model(
    "AssociateEmail_Expect",
    {
        "email": fields.String(),
        "status": fields.Boolean(),
        "item_type_ids": fields.String(),

    },
)

Associate_emails_subtypes = api.model(
    "associate_emails_subtypes",
    {"item_subtype": fields.Nested(Item_subtype, as_list=True)}
)
AssociateEmail = api.model(
    "associateEmail",
    {
        "id": fields.Integer(),
        "email": fields.String(),
        "status": fields.Boolean(),
        "associate_email_subtypes": fields.Nested(Associate_emails_subtypes, as_list=True),

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
