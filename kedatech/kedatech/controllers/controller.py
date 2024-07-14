from odoo import http
from odoo.http import request
import werkzeug.wrappers
import requests
import base64
import mimetypes
try:
    import simplejson as json
except ImportError:
    import json


def valid_response(status, data):
    return werkzeug.wrappers.Response(
        status=status,
        content_type='application/json; charset=utf-8',
        response=json.dumps(data),
    )

class MasterData(http.Controller):
    @http.route('/kedatech/data/create', type='http', csrf=False, auth="none", methods=['POST','GET'])
    def kedatech_data_create(self,**kwargs):
        name = kwargs.get('name')
        code = kwargs.get('code')
        mat_type = kwargs.get('type')
        buy_price = int(kwargs.get('buy_price'))
        partner_id = kwargs.get('partner_id')
        
        if buy_price < 100:
            return valid_response(
                200, {
                        'result': 'Buying Price must greate than 100'
                    }
                )

        OProduct = request.env['master.product']

        product_id = OProduct.sudo().search([('code','=', code)])
        if product_id:
             return valid_response(
                200, {
                        'status': "Fail",
                        'result': 'Product Code has been used in product %s' % product_id.name
                    }
                )

        product_id = OProduct.sudo().create({
            'name' : name,
            'code' : code,
            'type' : mat_type,
            'buy_price' : buy_price,
            'partner_id' : partner_id
            })

        if product_id:
            return valid_response(
                200, {
                        'status': "Success",
                        'result': 'Success Creating Product'
                    }
                )
        else:
            return valid_response(
                200, {
                        'status': "Success",
                        'result': 'Error Creating Product'
                    }
                )
    
    @http.route('/kedatech/data/update/<string:code>', type='http', csrf=False, auth="none", methods=['POST','GET'])
    def kedatech_data_update(self,code=None, **kwargs):
        if code:
            OProduct = request.env['master.product']
            product_id = OProduct.sudo().search([('code','=', code)])
            if product_id:
                if int(kwargs.get('buy_price')) < 100:
                     return valid_response(
                        200, {
                                'result': 'Buying Price must greate than 100'
                            }
                        )
                
                name = kwargs.get('name') or product_id.name
                mat_type = kwargs.get('type') or product_id.type
                buy_price = int(kwargs.get('buy_price')) or product_id.buy_price
                partner_id = kwargs.get('partner_id') or product_id.partner_id.id
        
                product_id.sudo().write({
                    'name' : name,
                    'type' : mat_type,
                    'buy_price' : buy_price,
                    'partner_id' : partner_id
                })
                return valid_response(
                    200, {
                            'status': "Succes",
                            'result': "Success Update Product %s" % code
                        }
                    )

            else:
                return valid_response(
                    200, {
                            'status': "Fail",
                            'result': "There is no any product that have this code %s" % code
                        }
                    )
        else:
            return valid_response(
                200, {
                        'status': "Fail",
                        'result': "Please input product code in end of endpoint"
                    }
                )

    @http.route('/kedatech/data/info/<string:code>', type='http', csrf=False, auth="none", methods=['GET'])
    def kedatech_data_info(self, code=None, **kwargs):
        if code:
            OProduct = request.env['master.product']
            product_id = OProduct.sudo().search([('code','=', code)])
            if product_id:
                return valid_response(
                    200, {
                            'status': "Succes",
                            'result': {
                                'name': product_id.name,
                                'code' : product_id.code,
                                'type': product_id.type,
                                'buy_price' : product_id.buy_price,
                                'partner_id' : product_id.partner_id.name
                            }
                        }
                    )

            else:
                return valid_response(
                    200, {
                            'status': "Fail",
                            'result': "There is no any product that have this code %s" % code
                        }
                    )
        else:
            return valid_response(
                200, {
                        'status': "Fail",
                        'result': "Please input product code in end of endpoint"
                    }
                )
    
    @http.route('/kedatech/data/delete/<string:code>', type='http', csrf=False, auth="none", methods=['POST'])
    def kedatech_data_delete(self, code=None, **kwargs):
        if code:
            OProduct = request.env['master.product']
            product_id = OProduct.sudo().search([('code','=', code)])
            if product_id:
                product_id.unlink()
                
                return valid_response(
                    200, {
                            'status': "Succes",
                            'result': "Product Deleted"
                        }
                    )

            else:
                return valid_response(
                    200, {
                            'status': "Fail",
                            'result': "There is no any product that have this code %s" % code
                        }
                    )
        else:
            return valid_response(
                200, {
                        'status': "Fail",
                        'result': "Please input product code in end of endpoint"
                    }
                )

