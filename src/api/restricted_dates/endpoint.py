from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.restricted_dates import RestrictedDates
from . import api, schema


@api.route("")
class RestrictedDatesList(Resource):
    @api.doc("Get all RestrictedDates")
    @api.marshal_list_with(schema.get_list_RestrictedDates)
    @auth
    def get(self):
        args = request.args.copy()
        all_rows, count = RestrictedDates.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.RestrictedDates_Expect)
    @api.marshal_list_with(schema.get_by_id_RestrictedDates)
    @auth
    def post(self):
        payload = api.payload
        restrictedDates = RestrictedDates(**payload)
        restrictedDates.insert()
        return response_structure(restrictedDates), 201


@api.route("/<int:restricted_dates_id>")
class restricted_dates_by_id(Resource):
    @api.doc("Get RestrictedDates by id")
    @api.marshal_list_with(schema.get_by_id_RestrictedDates)
    @auth
    def get(self, restricted_dates_id):
        restrictedDates = RestrictedDates.query_by_id(restricted_dates_id)
        return response_structure(restrictedDates), 200

    @api.doc("Delete method by id")
    @auth
    def delete(self, restricted_dates_id):
        RestrictedDates.delete(restricted_dates_id)
        return "ok", 200

    # @api.marshal_list_with(schema.get_by_id_responseVoucher)
    # @api.expect(schema.Voucher_Expect)
    # @auth
    # def patch(self, voucher_id):
    #     payload = api.payload
    #     Voucher.update(voucher_id, payload)
    #     voucher = Voucher.query_by_id(voucher_id)
    #     return response_structure(voucher), 200
