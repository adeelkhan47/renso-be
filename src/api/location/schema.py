from flask_restx import fields

from . import api

location_Expect = api.model(
    "Location_Expect",
    {
        "name": fields.String(),
        "description": fields.String(),
        "price_factor": fields.Integer(),

    },
)

Location = api.model(
    "Location",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "description": fields.String(),
        "price_factor": fields.Integer(),
        "is_deleted": fields.Boolean()

    },
)

get_list_responseLocation = api.model(
    "getAll_Locations",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Location, as_list=True),
    },
)
get_by_id_responseLocation = api.model(
    "getById_tag",
    {
        "objects": fields.Nested(Location),

    },
)
