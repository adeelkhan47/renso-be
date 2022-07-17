from flask_restx import fields

from . import api
from ..item_type.schema import Item_type

RestrictedDates_Expect = api.model(
    "RestrictedDates_Expect",
    {
        "start_date": fields.Date(),
        "end_date": fields.Date(),
        "item_type_id": fields.Integer(),
    },
)

RestrictedDates = api.model(
    "RestrictedDates",
    {
        "id": fields.Integer(),
        "start_date": fields.Date(),
        "end_date": fields.Date(),
    },
)

get_list_RestrictedDates = api.model(
    "getAll_RestrictedDates",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(RestrictedDates, as_list=True),
    },
)
get_by_id_RestrictedDates = api.model(
    "getById_RestrictedDates",
    {
        "objects": fields.Nested(RestrictedDates),

    },
)
