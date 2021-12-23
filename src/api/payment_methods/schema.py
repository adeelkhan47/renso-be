from flask_restx import fields

from . import api
from ..tax.schema import Tax

Tax_sc = api.model(
    "tax",
    {"tax": fields.Nested(Tax, as_list=True)}
)

PaymentMethod = api.model(
    "payment_method",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "status": fields.String(),
        "payment_tax": fields.Nested(Tax_sc, as_list=True),

    },
)

get_list_response = api.model(
    "getAll_payment_method",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(PaymentMethod, as_list=True),
    },
)
get_by_id_response = api.model(
    "getById_payment_method",
    {
        "objects": fields.Nested(PaymentMethod),

    },
)
