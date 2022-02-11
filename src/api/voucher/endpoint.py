from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.voucher import Voucher
from . import api, schema


@api.route("")
class VoucherList(Resource):
    @api.doc("Get all Vouchers")
    @api.marshal_list_with(schema.get_list_responseVoucher)
    def get(self):
        args = request.args
        all_rows, count = Voucher.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.Voucher_Expect)
    @api.marshal_list_with(schema.get_by_id_responseVoucher)
    def post(self):
        payload = api.payload
        voucher = Voucher(**payload)
        voucher.insert()
        return response_structure(voucher), 201


@api.route("/<int:voucher_id>")
class voucher_by_id(Resource):
    @api.doc("Get voucher by id")
    @api.marshal_list_with(schema.get_by_id_responseVoucher)
    def get(self, voucher_id):
        voucher = Voucher.query_by_id(voucher_id)
        return response_structure(voucher), 200

    @api.doc("Delete method by id")
    def delete(self, voucher_id):
        Voucher.delete(voucher_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseVoucher)
    @api.expect(schema.Voucher_Expect)
    def patch(self, voucher_id):
        payload = api.payload
        Voucher.update(voucher_id, payload)
        voucher = Voucher.query_by_id(voucher_id)
        return response_structure(voucher), 200
