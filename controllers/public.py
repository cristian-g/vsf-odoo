import logging
import json
import werkzeug.wrappers
from odoo import http
from odoo.http import request
from odoo.addons.restful.common import invalid_response, valid_response

_logger = logging.getLogger(__name__)

class PublicAPI(http.Controller):
    """."""

    def __init__(self):
        return

    @http.route('/api/products', methods=['GET'], type='http', auth='none', csrf=False)
    def products(self, **post):
        # Successful response:
        #return werkzeug.wrappers.Response(
            #status=200,
            #content_type='application/json; charset=utf-8',
            #headers=[('Cache-Control', 'no-store'),
            #         ('Pragma', 'no-cache')],
            #response=json.dumps({
            #    'products': 'list of products',
            #}),
        #)
        data = request.env['product.template'].sudo().search_read(
            domain=[], fields=['id', 'name', 'description', 'price', 'public_categ_ids'], offset=None, limit=None,
            order=None)
        if data:
            return valid_response(data)
        else:
            return invalid_response(data)

    @http.route('/api/categories', methods=['GET'], type='http', auth='none', csrf=False)
    def categories(self, **post):
        data = request.env['product.public.category'].sudo().search_read(
            domain=[],
            fields=['id', 'name', 'display_name', 'parent_id', 'child_id'],
            offset=None, limit=None,
            order=None)
        if data:
            return valid_response(data)
        else:
            return invalid_response(data)

    @http.route('/api/category_products', methods=['GET'], type='http', auth='none', csrf=False)
    def category_products(self, **payload):
        data = request.env['product.template'].sudo().search_read(
            domain=[('public_categ_ids', 'in', [payload.get('category_id')])],
            fields=['id', 'name', 'description', 'price', 'public_categ_ids'],
            offset=None,
            limit=None,
            order=None
        )
        if data:
            return valid_response(data)
        else:
            return invalid_response(data)

    @http.route('/api/stock', methods=['GET'], type='http', auth='none', csrf=False)
    def stock(self, **payload):

        product = request.env['product.product'].sudo().browse(int(payload.get('product_id')))
        available_qty = product.qty_available

        # For specific warehouse / location:
        #available_qty = product.with_context({'warehouse': WAREHOUSE_ID}).qty_available
        #available_qty = product.with_context({'location': LOCATION_ID}).qty_available
        # Source: https://www.odoo.com/es_ES/forum/ayuda-1/question/how-to-get-product-quantity-109870

        return valid_response({
            'stock': available_qty
        })

    @http.route('/api/signup', methods=['POST'], type='http', auth='none', csrf=False)
    def signup(self, **payload):
            resource = request.env['res.users'].sudo().create({
                      'name': payload.get('name'),
                      'login': payload.get('email'),
                      'company_ids': [1],
                      'company_id': 1,
                      'new_password': payload.get('password'),
                      'is_company' : False,
                       'groups_id': [9]
                  })
            data = {'id': resource.id}
            request.env.cr.execute('INSERT INTO res_company_users_rel(user_id, cid) VALUES('+str(resource.id)+', 1)')
            if resource:
                return valid_response(data)
            else:
                return invalid_response(data)
