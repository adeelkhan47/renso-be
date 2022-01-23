from flask_restx import fields

from . import api
Tax_expect = api.model(
    "Tax_expect",
    {
        "name": fields.String(),
        "percentage": fields.Integer(),
        "description": fields.String(),
    },
)
Tax = api.model(
    "tax",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "percentage": fields.Integer(),
        "description": fields.String(),
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
