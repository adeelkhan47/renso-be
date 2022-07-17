from flask_restx import fields

from ..tax.schema import Tax
from . import api

Tax_nested = api.model(
    "tax",
    {"tax": fields.Nested(Tax, as_list=True)}
)

PaymentMethodExpect = api.model(
    "PaymentMethodExpect",
    {
        "name": fields.String(),
        "description": fields.String(),
        "status": fields.Boolean(),
        "tax_ids": fields.String(),

    },
)
PaymentMethod = api.model(
    "payment_method",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "description": fields.String(),
        "status": fields.Boolean(),
        "payment_tax": fields.Nested(Tax_nested, as_list=True),
        "is_deleted": fields.Boolean()

    },
)

get_list_responsePaymentMethod = api.model(
    "getAll_payment_method",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(PaymentMethod, as_list=True),
    },
)
get_by_id_responsePaymentMethod = api.model(
    "getById_payment_method",
    {
        "objects": fields.Nested(PaymentMethod),

    },
)
