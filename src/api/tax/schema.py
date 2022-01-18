from flask_restx import fields

from . import api
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
