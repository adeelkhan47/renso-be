from flask_restx import fields

from . import api
from ..company.schema import Company
from ..item_type.schema import Item_type

TaxInSubtype = api.model(
    "tax",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "percentage": fields.Integer(),
        "description": fields.String(),
    },
)
Item_subtype_Expect = api.model(
    "item_subtype_expect",
    {

        "name": fields.String(),
        "price": fields.Float(),
        "person": fields.Integer(),
        "item_type_id": fields.Integer(),
        "company_id": fields.Integer(),
        "image": fields.String(),
        "least_price": fields.Float(),
        "discount_after_higher_price": fields.Integer(),
        "same_price_days": fields.Integer(),
        "show_description": fields.Boolean(),
        "description": fields.String(),
        "is_deleted": fields.Boolean()

    },
)

subtype_taxs = api.model(
    "subtype_taxs",
    {"tax": fields.Nested(TaxInSubtype, as_list=True)}
)
Item_subtype = api.model(
    "item_sub_type",
    {
        "id": fields.Integer(),
        "price": fields.Float(),
        "name": fields.String(),
        "image": fields.String(),
        "person": fields.Integer(),
        "item_type": fields.Nested(Item_type),
        "company": fields.Nested(Company, skip_none=True),
        "least_price": fields.Float(),
        "discount_after_higher_price": fields.Integer(),
        "same_price_days": fields.Integer(),
        "show_description": fields.Boolean(),
        "description": fields.String(),
        "itemSubTypeTaxs": fields.Nested(subtype_taxs, as_list=True)
    },
)

Availability_Response = api.model(
    "availability_response",
    {
        "item_sub_type_object": fields.Nested(Item_subtype),
        "available_item_ids": fields.List(fields.Integer()),
    }

)
error = api.model(
    "Error",
    {

        "msg": fields.String(),

    },
)

get_list_responseItem_Subtype = api.model(
    "getAll_item_type",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Item_subtype, as_list=True),
    },
)

get_list_Availability_responseItem_Subtype_ = api.model(
    "getAll_Availability_item_type",
    {
        "total_rows": fields.Integer(),
        "objects": fields.List(fields.Nested(Availability_Response, as_list=True)),
        "error": fields.Nested(error, allow_null=True),
    },
)
get_by_id_responseItem_Subtype = api.model(
    "getById_item_type",
    {
        "objects": fields.Nested(Item_subtype),

    },
)
