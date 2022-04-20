from flask import g
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure
from decorator.authorization import auth
from model.front_end_configs import FrontEndCofigs
from . import api, schema


@api.route("")
class fetch_logo_by_user_id(Resource):
    @api.marshal_list_with(schema.get_by_id_FE_LOGO)
    @auth
    def get(self):
        logo = FrontEndCofigs.get_by_user_id(g.current_user.id)
        if not logo:
            raise NotFound("front_end_configs Not Found.")
        return response_structure(logo), 200

    @api.marshal_list_with(schema.get_by_id_FE_LOGO)
    @api.expect(schema.FrontEndExpect)
    @auth
    def patch(self):
        data = api.payload.copy()
        config = FrontEndCofigs.get_by_user_id(g.current_user.id)
        FrontEndCofigs.update(config.id, data)
        return response_structure(FrontEndCofigs.query_by_id(config.id)), 200
