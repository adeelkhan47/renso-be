from flask_restx import fields

from . import api

Voucher_Expect = api.model(
    "Voucher_Expect",
    {
        "code": fields.String(),
        "description": fields.String(),
        "price_factor": fields.Integer(),
        "status": fields.Boolean(),
        "counter": fields.Integer(),
    },
)

Voucher = api.model(
    "Voucher",
    {
        "id": fields.Integer(),
        "counter": fields.Integer(),
        "code": fields.String(),
        "description": fields.String(),
        "price_factor": fields.Integer(),
        "status": fields.Boolean(),
    },
)

get_list_responseVoucher = api.model(
    "getAll_Voucher",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Voucher, as_list=True),
    },
)
get_by_id_responseVoucher = api.model(
    "getById_Voucher",
    {
        "objects": fields.Nested(Voucher),

    },
)
