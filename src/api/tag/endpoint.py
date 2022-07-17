from flask import g
from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.tag import Tag
from . import api, schema


@api.route("")
class TagList(Resource):
    @api.doc("Get all Tag")
    @api.marshal_list_with(schema.get_list_responseTag)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        args["is_deleted:eq"] = "False"
        all_rows, count = Tag.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.Tag_Expect)
    @api.marshal_list_with(schema.get_by_id_responseTag)
    @auth
    def post(self):
        payload = api.payload
        name = payload.get("name")
        color = payload.get("color")
        description = payload.get("description")
        tag = Tag(name, description, color, g.current_user.id)
        tag.insert()
        return response_structure(tag), 201


@api.route("/<int:tag_id>")
class tag_by_id(Resource):
    @api.doc("Get tax by id")
    @api.marshal_list_with(schema.get_by_id_responseTag)
    @auth
    def get(self, tag_id):
        tag = Tag.query_by_id(tag_id)
        return response_structure(tag), 200

    @api.doc("Delete method by id")
    @auth
    def delete(self, tag_id):
        Tag.soft_delete(tag_id)
        return "ok", 200
