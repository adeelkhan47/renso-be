from flask import g
from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.company import Company
from . import api, schema


@api.route("")
class Company_list(Resource):
    @api.doc("Get all Company")
    @api.marshal_list_with(schema.get_list_responseCompany)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        args["is_deleted:eq"] = "False"
        all_items, count = Company.filtration(args)
        return response_structure(all_items, count), 200

    @api.marshal_list_with(schema.get_list_responseCompany, skip_none=True)
    @api.expect(schema.CompanyExpect, validate=True)
    @auth
    def post(self):
        payload = api.payload
        payload["user_id"] = str(g.current_user.id)
        company = Company(**payload)
        company.insert()
        return response_structure(company), 201


@api.route("/<int:company_id>")
class item_by_id(Resource):
    @api.doc("Get all Companies")
    @api.marshal_list_with(schema.get_by_id_responseCompany)
    @auth
    def get(self, company_id):
        company = Company.query_by_id(company_id)
        return response_structure(company), 200

    @api.doc("Delete Companies by id")
    @auth
    def delete(self, company_id):
        Company.soft_delete(company_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseCompany, skip_none=True)
    @api.expect(schema.CompanyExpect)
    @auth
    def patch(self, company_id):
        data = api.payload.copy()
        if "is_deleted" not in data.keys():
            data["is_deleted"] = False
        Company.update(company_id, data)
        item = Company.query_by_id(company_id)
        return response_structure(item), 200
