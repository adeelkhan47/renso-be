from flask import g
from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.season import Season
from model.season_item_type import SeasonItemTypes
from . import api, schema


@api.route("")
class Season_list(Resource):
    @api.doc("Get all Seasons")
    @api.marshal_list_with(schema.get_list_responseSeason)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        all_items, count = Season.filtration(args)
        return response_structure(all_items, count), 200

    @api.marshal_list_with(schema.get_by_id_responseSeason, skip_none=True)
    @api.expect(schema.SeasonExpect, validate=True)
    @auth
    def post(self):
        payload = api.payload
        start_time = payload.get("start_time")
        end_time = payload.get("end_time")
        price_factor = payload.get("price_factor")
        season = Season(start_time, end_time, price_factor, g.current_user.id)
        season.insert()
        if "season_item_types" in payload.keys():
            if request.json.get("season_item_types") != "":
                item_type_ids = request.json.get("season_item_types").split(",")
                for each in item_type_ids:
                    SeasonItemTypes(item_type_id=each, season_id=season.id).insert()
        return response_structure(season), 201


@api.route("/<int:season_id>")
class booking_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseSeason)
    @auth
    def get(self, season_id):
        season = Season.query_by_id(season_id)
        return response_structure(season), 200

    @auth
    def delete(self, season_id):
        Season.delete(season_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseSeason, skip_none=True)
    @api.expect(schema.SeasonExpect, validate=True)
    @auth
    def patch(self, season_id):
        payload = api.payload
        data = payload.copy()
        if "season_item_types" in payload.keys():
            SeasonItemTypes.delete_by_season_id(season_id)
            if request.json.get("season_item_types") != "":
                item_type_ids = request.json.get("season_item_types").split(",")
                for each in item_type_ids:
                    SeasonItemTypes(item_type_id=each, season_id=season_id).insert()
            del data["season_item_types"]
        Season.update(season_id, data)
        season = Season.query_by_id(season_id)
        return response_structure(season), 200
