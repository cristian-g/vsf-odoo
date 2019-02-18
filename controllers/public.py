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
