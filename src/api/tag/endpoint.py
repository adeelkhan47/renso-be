from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.tag import Tag
from . import api, schema


@api.route("")
class TagList(Resource):
    @api.doc("Get all Tag")
    @api.marshal_list_with(schema.get_list_responseTag)
    def get(self):
        args = request.args
        all_rows, count = Tag.filtration(args)
        return response_structure(all_rows, count), 200

    @api.param("name", required=True)
    @api.param("description")
    @api.param("color", required=True)
    def post(self):
        payload = api.payload
        name = payload.get("name")
        color = payload.get("color")
        description = payload.get("description")
        tag = Tag(name, description, color)
        tag.insert()
        return "ok", 201


@api.route("/<int:tag_id>")
class tag_by_id(Resource):
    @api.doc("Get tax by id")
    @api.marshal_list_with(schema.get_by_id_responseTag)
    def get(self, tag_id):
        tag = Tag.query_by_id(tag_id)
        return response_structure(tag), 200

    @api.doc("Delete method by id")
    def delete(self, tag_id):
        Tag.delete(tag_id)
        return "ok", 200
