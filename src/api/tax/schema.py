from flask_restx import fields

from . import api
from ..item_subtype.schema import Item_subtype

Tax_expect = api.model(
    "Tax_expect",
    {
        "name": fields.String(),
        "percentage": fields.Integer(),
        "description": fields.String(),
        "item_sub_type_ids": fields.String()
    },
)
Item_SubTypes_in = api.model(
    "item_subtypes",
    {"item_subtype": fields.Nested(Item_subtype, as_list=True)}
)
Tax = api.model(
    "tax",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "percentage": fields.Integer(),
        "description": fields.String(),
        "itemSubTypeTaxs": fields.Nested(Item_SubTypes_in, as_list=True),
        "is_deleted": fields.Boolean()
    },
)

get_list_responseTax = api.model(
    "getAll",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Tax, as_list=True),
    },
)
get_by_id_responseTax = api.model(
    "getById_tax",
    {
        "objects": fields.Nested(Tax),

    },
)
