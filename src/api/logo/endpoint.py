from flask import g
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure
from decorator.authorization import auth
from model.logo import Logo
from . import api, schema


@api.route("")
class fetch_logo_by_user_id(Resource):
    @api.marshal_list_with(schema.get_by_id_FE_LOGO)
    @auth
    def get(self):
        logo = Logo.get_by_user_id(g.current_user.id)
        if not logo:
            raise NotFound("logo Not Found.")
        return response_structure(logo), 200
        ø

    @api.marshal_list_with(schema.get_by_id_FE_LOGO)
    @api.expect(schema.Logo_Expect)
    @auth
    def patch(self):
        data = api.payload.copy()
        logo = Logo.get_by_user_id(g.current_user.id)
        Logo.update(logo.id, data)
        return response_structure(Logo.query_by_id(logo.id)), 200
