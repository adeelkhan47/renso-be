from flask_restx import fields

from . import api

SeasonExpect = api.model(
    "seasonExpect",
    {
        "start_time": fields.DateTime(),
        "end_time": fields.DateTime(),
        "price_factor": fields.Integer(),
        "season_item_types": fields.String()
    },
)

Season = api.model(
    "season",
    {
        "id": fields.Integer(),
        "start_time": fields.DateTime(),
        "end_time": fields.DateTime(),
        "price_factor": fields.Integer()
    },
)
error = api.model(
    "Error",
    {

        "msg": fields.String(),

    },
)

get_list_responseSeason = api.model(
    "getAllSeason",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Season, as_list=True, skip_none=True, allow_null=True),
        "error": fields.Nested(error, allow_null=True),
    },
)
get_by_id_responseSeason = api.model(
    "getByIdSeason",
    {
        "objects": fields.Nested(Season, skip_none=True, allow_null=True),
        "error": fields.Nested(error, allow_null=True),

    },
)
