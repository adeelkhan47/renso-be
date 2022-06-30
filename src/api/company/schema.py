from flask_restx import fields

from . import api
CompanyExpect = api.model(
    "companyExpect",
    {
        "name": fields.String(),
        "street": fields.String(),
        "street_number": fields.String(),
        "zipcode": fields.String(),
        "city": fields.String(),
        "commercial_registered_number": fields.String(),
        "legal_representative": fields.String(),
        "email_for_taxs": fields.String(),
        "company_tax_number": fields.String(),
        "bate_number": fields.Integer(),
        "email": fields.String(),
    },
)

Company = api.model(
    "company",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "street": fields.String(),
        "street_number": fields.String(),
        "zipcode": fields.String(),
        "city": fields.String(),
        "commercial_registered_number": fields.String(),
        "legal_representative": fields.String(),
        "email_for_taxs": fields.String(),
        "company_tax_number": fields.String(),
        "email": fields.String(),
        "bate_number": fields.Integer(),
        #"item_subtype": fields.Nested(Item_subtype),
        #"sub_category_company": fields.Nested(tags, as_list=True),
    },
)

get_list_responseCompany = api.model(
    "getAll_company",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Company, as_list=True),
    },
)
get_by_id_responseCompany = api.model(
    "getById_company",
    {
        "objects": fields.Nested(Company, skip_none=True),

    },
)
