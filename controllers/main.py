import functools
import logging
import json
import werkzeug.wrappers
import collections
from odoo import http
from odoo.http import request
from odoo.addons.vue_storefront.common import valid_response, invalid_response, extract_arguments, simple_response
from odoo.addons.vue_storefront.controllers.json_types import JSONTypes
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

def validate_token(func):
    """."""
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        """."""
        #access_token = request.httprequest.headers.get('access_token')
        access_token = kwargs.get('token')
        if not access_token:
            return invalid_response('access_token_not_found', 'missing access token in request header', 401)
        access_token_data = request.env['api.access_token'].sudo().search(
            [('token', '=', access_token)], order='id DESC', limit=1)

        if access_token_data.find_one_or_create_token(user_id=access_token_data.user_id.id) != access_token:
            return invalid_response('access_token', 'token seems to have expired or invalid', 401)

        request.session.uid = access_token_data.user_id.id
        request.uid = access_token_data.user_id.id
        return func(self, *args, **kwargs)
    return wrap

def validate_optional_token(func):
    """."""
    @functools.wraps(func)
    def optional_wrap(self, *args, **kwargs):
        """."""
        #access_token = request.httprequest.headers.get('access_token')
        access_token = kwargs.get('token')

        if access_token:

            access_token_data = request.env['api.access_token'].sudo().search(
                [('token', '=', access_token)], order='id DESC', limit=1)

            if access_token_data.find_one_or_create_token(user_id=access_token_data.user_id.id) != access_token:
                return invalid_response('access_token', 'token seems to have expired or invalid', 401)

            request.session.uid = access_token_data.user_id.id
            request.uid = access_token_data.user_id.id

        return func(self, *args, **kwargs)
    return optional_wrap

_routes = [
    '/api/<model>',
    '/api/<model>/<id>',
    '/api/<model>/<id>/<action>'
]

class PrivateAPIController(http.Controller):
    """."""

    def __init__(self):
        self._model = 'ir.model'

    @validate_token
    @http.route(_routes, type='http', auth="none", methods=['GET'], csrf=False)
    def get(self, model=None, id=None, **payload):
        ioc_name = model
        model = request.env[self._model].sudo().search(
            [('model', '=', model)], limit=1)
        if model:
            domain, fields, offset, limit, order = extract_arguments(
                payload)
            data = request.env[model.model].sudo().search_read(
                domain=domain, fields=['id', 'name', 'description', 'price', 'public_categ_ids'], offset=offset, limit=limit, order=order)
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response('invalid object model', 'The model %s is not available in the registry.' % ioc_name)

    @validate_token
    @http.route('/api/user/me', type='http', auth="none", methods=['OPTIONS'], csrf=False)
    def profile_options(self, model=None, id=None, **payload):
        data = {
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )

    @validate_token
    @http.route('/api/user/me', type='http', auth="none", methods=['GET'], csrf=False)
    def profile(self, **payload):

        data = request.env['res.users'].sudo().search_read(domain=[('id', '=', request.session.uid)], fields=['id', 'login'], offset=None, limit=1, order=None)
        if data:
            #return valid_response(data)
            user_info = data[0]
            response_data = {
                "code":200,
                "result":
                    self.user_json(user_info.get('login'))
            }
            return simple_response(response_data, 200)
        else:
            return invalid_response(data)

    @validate_token
    @http.route('/api/user/me', type='http', auth="none", methods=['POST'], csrf=False)
    def profile_edit(self, **payload):

        body = request.httprequest.get_data()
        body_json = json.loads(body.decode("utf-8"))

        data = request.env['res.users'].sudo().search_read(domain=[('id', '=', request.session.uid)], fields=['id', 'login'], offset=None, limit=1, order=None)
        if data:
            #return valid_response(data)
            user_info = data[0]
            response_data = {
                "code":200,
                "result":
                    self.user_json(user_info.get('login'))
            }
            return simple_response(response_data, 200)
        else:
            return invalid_response(data)

    @validate_token
    @http.route('/api/edit_profile', type='http', auth="none", methods=['PATCH'], csrf=False)
    def edit_profile(self, **payload):
        user_data = request.env['res.users'].sudo().search_read(
            domain=[('id', '=', request.session.uid)],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )
        partner_data = request.env['res.partner'].sudo().search_read(
            domain=[('id', '=', user_data[0].get('partner_id')[0])],
            fields=['email'],
            offset=None,
            limit=1,
            order=None
        )
        request.env['res.partner'].sudo().search([('id', '=', user_data[0].get('partner_id')[0])]).write({
            'name': payload.get('name'),
            'email': payload.get('email'),
            'phone': payload.get('phone'),
            'company_name': payload.get('company_name'),
            'commercial_company_name': payload.get('company_name'),
            'vat': payload.get('nif'),
            'street': payload.get('street'),
            'city': payload.get('city'),
            'zip': payload.get('zip'),
            'country_id': 68,
            'state_id': payload.get('state_id'),
        })
        if payload.get('email') != partner_data[0].get('email'):
            # Running this will cause to expire the token on web session (web module)
            request.env['res.users'].sudo().search([('id', '=', request.session.uid)]).write({
                'login': payload.get('email'),
            })

    @validate_token
    @http.route('/api/user/order-history', type='http', auth="none", methods=['GET'], csrf=False)
    def order_history(self, **payload):

        user_data = request.env['res.users'].sudo().search_read(
            domain=[('id', '=', request.session.uid)],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )
        orders = request.env['sale.order'].sudo().search_read(
            domain=[
                ('partner_id', '=', user_data[0].get('partner_id')[0]),
                ('state', '=', 'sale'),
            ],
            fields=[
                'id',
                'confirmation_date',
                'amount_total',
            ],
            offset=None,
            limit=None,
            order='create_date DESC'
        )
        orders_array = []
        for order in orders:
            order_id = int(order.get('id'))
            confirmation_date = str(order.get('confirmation_date'))
            amount_total = order.get('amount_total')
            orders_array.append(JSONTypes.order_json(
                order_id,
                confirmation_date,
                amount_total,
            ))

        return simple_response(
            {
                "code": 200,
                "result": {
                    "items": orders_array,
                    "search_criteria": {
                        "filter_groups": [
                            {
                                "filters": [
                                    {
                                        "field": "customer_email",
                                        "value": "pkarwatka28@example.com",
                                        "condition_type": "eq"
                                    }
                                ]
                            }
                        ]
                    },
                    "total_count": 61
                }
            }
        )

    @http.route('/api/cart/create', type='http', auth="none", methods=['OPTIONS'], csrf=False)
    def cart_create_options(self, **payload):
        data = {
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )

    @validate_optional_token
    @http.route('/api/cart/create', type='http', auth="none", methods=['POST'], csrf=False)
    def cart_create(self, **payload):

        if request.session.uid:
            user_data = request.env['res.users'].sudo().search_read(
                domain=[('id', '=', request.session.uid)],
                fields=['partner_id'],
                offset=None,
                limit=1,
                order=None
            )
            partner_id = int(user_data[0].get('partner_id')[0])
            sale_order = request.env['sale.order'].sudo().create({
                'currency_id': 1,
                'date_order': datetime.now(),
                'name': 'SO',
                'partner_id': partner_id,
                'partner_invoice_id': partner_id,
                'partner_shipping_id': partner_id,
                'picking_policy': 'direct',
                'pricelist_id': 1,
                'warehouse_id': 1,
                'state': 'draft',
                'team_id': 2,
            })
            if sale_order:
                return simple_response(
                    {
                        "code": 200,
                        "result": str(sale_order.id)
                    }
                )
            else:
                return invalid_response(
                    {
                        "code": 500,
                    }
                )
        else:
            sale_order = request.env['sale.order'].sudo().create({
                'currency_id': 1,
                'date_order': datetime.now(),
                'name': 'SO',
                'partner_id': 4,
                'partner_invoice_id': 4,
                'partner_shipping_id': 4,
                'picking_policy': 'direct',
                'pricelist_id': 1,
                'warehouse_id': 1,
                'state': 'draft',
                'team_id': 2,
            })
            if sale_order:
                return simple_response(
                    {
                        "code": 200,
                        "result": str(sale_order.id)
                    }
                )
            else:
                return invalid_response(
                    {
                        "code": 500,
                    }
                )

    @http.route('/api/cart/delete', type='http', auth="none", methods=['OPTIONS'], csrf=False)
    def cart_delete_options(self, **payload):
        data = {
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )

    @http.route('/api/cart/delete', type='http', auth="none", methods=['POST'], csrf=False)
    def cart_delete(self, **payload):

        #body = request.httprequest.get_data()
        #body_json = json.loads(body.decode("utf-8"))

        return simple_response(
            {
                "code": 200,
                "result": True
            }
        )

    @http.route('/api/cart/pull', type='http', auth="none", methods=['OPTIONS'], csrf=False)
    def cart_options(self, **payload):
        data = {
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )

    @validate_optional_token
    @http.route('/api/cart/pull', type='http', auth="none", methods=['GET'], csrf=False)
    def cart(self, **payload):

        cart_id = int(payload.get('cartId'))

        # if request.session.uid:

        cart_lines = request.env['sale.order.line'].sudo().search_read(
            domain=[('order_id', '=', cart_id)],
            fields=[
                'id',
                'name',
                'invoice_status',
                'price_unit',
                'price_subtotal',
                'price_tax',
                'price_total',
                'price_reduce',
                'price_reduce_taxinc',
                'price_reduce_taxexcl',
                'discount',
                'product_id',
                'product_uom_qty',
            ],
            offset=None,
            limit=None,
            order='id DESC'
        )

        items = []
        for line in cart_lines:

            product_id = line['product_id'][0]

            # Prepare configurable_item_options
            product_data = request.env['product.product'].sudo().search_read(
                domain=[('id', '=', product_id)],
                fields=['attribute_value_ids'],
                offset=None,
                limit=None,
                order=None)
            configurable_item_options = []
            value_ids = product_data[0]['attribute_value_ids']
            for value_id in value_ids:
                attribute_value = request.env['product.attribute.value'].sudo().search_read(
                    domain=[('id', '=', value_id)],
                    fields=['attribute_id'],
                    offset=None,
                    limit=None,
                    order=None)
                attribute_id = attribute_value[0]['attribute_id'][0]
                configurable_item_options.append(
                    self.configurable_item_option_json(
                        str(attribute_id),
                        int(value_id)
                    )
                )

            items.append(self.cart_item_json(
                line['name'],
                product_id,
                configurable_item_options,
            ))

        return simple_response(
            {
                "code": 200,
                "result": items,
                "cart_id": int(payload.get('cartId')),
            }
        )

    def cart_item_json(self, name, item_id, configurable_item_options):
        result = {
          "item_id": item_id,
          # "sku": "WS08-XS-Red",
          "sku": str(item_id),
          "qty": 1,
          "name": name,
          "price": 32,
          "product_type": "configurable",
          "quote_id": "dceac8e2172a1ff0cfba24d757653257",
          "product_option": {
            "extension_attributes": {
              "configurable_item_options": configurable_item_options
            }
          }
        }
        return result

    def configurable_item_option_json(self, option_id, option_value):
        result = {
            "option_id": option_id,
            "option_value": option_value
        }
        return result

    def user_json(self, email):
        return {
            "id":158,
            "group_id":1,
            "default_shipping":"67",
            "created_at":"2018-02-28 12:05:39",
            "updated_at":"2018-03-29 10:46:03",
            "created_in":"Default Store View",
            "email": email,
            "firstname":"Piotr",
            "lastname":"Karwatka",
            "store_id":1,
            "website_id":1,
            "addresses":[
                    {
                        "id":67,
                        "customer_id":158,
                        "region":
                            {
                                "region_code":None,
                                "region":None,
                                "region_id":0
                            },
                        "region_id":0,
                        "country_id":"PL",
                        "street": ["Street name","13"],
                        "telephone":"",
                        "postcode":"41-157",
                        "city":"Wrocław",
                        "firstname":"John","lastname":"Murphy",
                        "default_shipping":True
                    }],
            "disable_auto_group_change":0
        }

    @http.route('/api/cart/update2', type='http', auth="none", methods=['OPTIONS'], csrf=False)
    def edit_quantity_options(self, **payload):
        data = {
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )

    @validate_optional_token
    @http.route('/api/cart/update2', type='http', auth="none", methods=['POST'], csrf=False)
    def edit_quantity(self, **payload):

        payload_line_id = payload.get('line_id')
        payload_quantity = payload.get('quantity')

        response = {
            "code": 200,
            "result":
                {
                    "item_id": 5853,
                    "sku": "MS10-XS-Black",
                    "qty": 2,
                    "name": "Logan  HeatTec&reg; Tee-XS-Black",
                    "price": 24,
                    "product_type": "simple",
                    "quote_id": "81668"
                }
        }

        return simple_response(
            response
        )

        # Check if line is related to authenticated user
        line_data = request.env['sale.order.line'].sudo().search_read(
            domain=[('id', '=', payload_line_id)],
            fields=['order_id'],
            offset=None,
            limit=1,
            order=None
        )
        order_data = request.env['sale.order'].sudo().search_read(
            domain=[('id', '=', line_data[0].get('order_id')[0])],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )
        user_data = request.env['res.users'].sudo().search_read(
            domain=[('id', '=', request.session.uid)],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )
        if order_data[0].get('partner_id') != user_data[0].get('partner_id'):
            return invalid_response('params', {'errors': ['Unauthorized']})

        request.env['sale.order.line'].sudo().search([('id', '=', payload_line_id)]).write({
            'product_uom_qty': payload_quantity,
        })

    @validate_token
    @http.route('/api/remove_line', type='http', auth="none", methods=['DELETE'], csrf=False)
    def remove_line(self, **payload):

        # Check if line is related to authenticated user
        line_data = request.env['sale.order.line'].sudo().search_read(
            domain=[('id', '=', payload.get('line_id'))],
            fields=['order_id'],
            offset=None,
            limit=1,
            order=None
        )
        order_data = request.env['sale.order'].sudo().search_read(
            domain=[('id', '=', line_data[0].get('order_id')[0])],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )
        user_data = request.env['res.users'].sudo().search_read(
            domain=[('id', '=', request.session.uid)],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )
        if order_data[0].get('partner_id') != user_data[0].get('partner_id'):
            return invalid_response('params', {'errors': ['Unauthorized']})

        # Remove line
        record = request.env['sale.order.line'].sudo().search([('id', '=', payload.get('line_id'))])
        if record:
            record.unlink()
            return valid_response('line %s has been successfully deleted' % record.id)
        else:
            return invalid_response('missing_line', 'line with id %s could not be found' % payload.get('line_id'), 404)

    @http.route('/api/cart/update', type='http', auth="none", methods=['OPTIONS'], csrf=False)
    def update_cart_options(self, **payload):
        data = {
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )

    @validate_optional_token
    @http.route('/api/cart/update', methods=['POST'], type='http', auth='none', csrf=False)
    def update_cart(self, **payload):

        body = request.httprequest.get_data()
        payload = json.loads(body.decode("utf-8"))

        # We need: product id
        # We have: product template id and product_attribute_value_id s

        # Use received product_tmpl_id to retrieve product ids from product.product
        received_product_tmpl_id = int(payload.get('cartItem').get('sku'))

        configurable_item_options = payload.get('cartItem').get('product_option').get('extension_attributes').get('configurable_item_options')

        desired_options_array = []
        for configurable_item_option in configurable_item_options:
            desired_options_array.append(
                int(configurable_item_option.get('option_value'))
            )

        product_templates = request.env['product.template'].sudo().search_read(
            domain=[('id', '=', received_product_tmpl_id)],
            fields=['name'],
            offset=None,
            limit=None,
            order=None)
        product_template_name = product_templates[0]["name"]

        products = request.env['product.product'].sudo().search_read(
            domain=[('product_tmpl_id', '=', received_product_tmpl_id)],
            fields=['id', 'attribute_value_ids'],
            offset=None,
            limit=None,
            order=None)

        desired_product_id = -1

        for product in products:

            actual_options_array = []

            value_ids = product['attribute_value_ids']
            for value_id in value_ids:
                actual_options_array.append(value_id)

            # If product_attribute_value_id s match with the received ones, this product id is the desired one
            desired = collections.Counter(desired_options_array) == collections.Counter(actual_options_array)

            if desired:
                desired_product_id = product['id']

        desired_quantity = 1

        user_data = request.env['res.users'].sudo().search_read(
            domain=[('id', '=', request.session.uid)],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )

        order_id = -1
        if request.session.uid:
            user_data = request.env['res.users'].sudo().search_read(
                domain=[('id', '=', request.session.uid)],
                fields=['partner_id'],
                offset=None,
                limit=1,
                order=None
            )
            orders = request.env['sale.order'].sudo().search_read(
                domain=[('partner_id', '=', user_data[0].get('partner_id')[0])],
                fields=['id'],
                offset=None,
                limit=1,
                order='create_date DESC'
            )
            order_id = int(orders[0].get('id'))
        else:
            order_id = int(payload.get('cartItem').get('quoteId'))

        order_line = request.env['sale.order.line'].sudo().create({
            'order_id': order_id,
            'product_id': desired_product_id,
            'product_uom_qty': desired_quantity,
            'customer_lead': 0.0,
            'name': product_template_name,
            'price_unit': 100.0,
        })

        response = {
            "code": 200,
            "result": {}
        }
        return simple_response(
            response
        )

    @validate_token
    @http.route('/api/set_shipping', type='http', auth="none", methods=['PATCH'], csrf=False)
    def set_shipping(self, **payload):
        user_data = request.env['res.users'].sudo().search_read(
            domain=[('id', '=', request.session.uid)],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )
        order_data = request.env['sale.order'].sudo().search_read(
            domain=[('partner_id', '=', user_data[0].get('partner_id')[0])],
            fields=['id'],
            offset=None,
            limit=1,
            order='create_date DESC'
        )
        request.env['sale.order'].sudo().search([('id', '=', order_data[0].get('id'))]).write({
            'partner_shipping_id': user_data[0].get('partner_id')[0],
        })

    @validate_token
    @http.route('/api/orders', type='http', auth="none", methods=['GET'], csrf=False)
    def orders(self, **payload):
        user_data = request.env['res.users'].sudo().search_read(
            domain=[('id', '=', request.session.uid)],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )
        orders = request.env['sale.order'].sudo().search_read(
            domain=[
                ('partner_id', '=', user_data[0].get('partner_id')[0]),
                ('state', '=', 'sent'),
            ],
            fields=[
                'id',
                'state',
                #'date_order',
                'require_payment',
                #'create_date',
                #'confirmation_date',
                'amount_untaxed',
                'amount_tax',
                'amount_total',
                #'write_date',
            ],
            offset=None,
            limit=None,
            order='create_date DESC'
        )
        for order in orders:
            order['lines'] = request.env['sale.order.line'].sudo().search_read(
                domain=[('order_id', '=', order['id'])],
                fields=[
                    'id',
                    'name',
                    'invoice_status',
                    'price_unit',
                    'price_subtotal',
                    'price_tax',
                    'price_total',
                    'price_reduce',
                    'price_reduce_taxinc',
                    'price_reduce_taxexcl',
                    'discount',
                    'product_id',
                    'product_uom_qty',
                ],
                offset=None,
                limit=None,
                order='id ASC'
            )
        return valid_response(orders)

    @validate_token
    @http.route('/api/change_password', type='http', auth="none", methods=['PATCH'], csrf=False)
    def change_password(self, **payload):
        request.env['res.users'].sudo().search([('id', '=', request.session.uid)]).write({'password': payload.get('password')})

    @http.route('/api/order', methods=['OPTIONS'], type='http', auth='none', csrf=False)
    def order_options(self, **payload):
        data = {
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )

    @http.route('/api/order', methods=['POST'], type='http', auth='none', csrf=False)
    def order(self, **payload):

        body = request.httprequest.get_data()
        body_json = json.loads(body.decode("utf-8"))
        # cart_id = int(payload.get('cart_id'))
        cart_id = int(body_json.get('cart_id'))

        request.env['sale.order'].sudo().search([
            ('id', '=', cart_id)
        ]).write({
            'confirmation_date': datetime.now(),
            'state': 'sale',
        })

        data = {
            "code": 200,
            "result": "OK"
        }
        return simple_response(data)

    @http.route('/api/cart/shipping-methods', methods=['OPTIONS'], type='http', auth='none', csrf=False)
    def shipping_methods_options(self, **payload):
        data = {
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )

    @http.route('/api/cart/shipping-methods', methods=['POST'], type='http', auth='none', csrf=False)
    def shipping_methods(self, **payload):

        body = request.httprequest.get_data()
        body_json = json.loads(body.decode("utf-8"))

        data = {
            "code":200,
            "result":
            [
                {
                    "carrier_code":"flatrate",
                    "method_code":"flatrate",
                    "carrier_title":"Flat Rate",
                    "method_title":"Fixed",
                    "amount":5,
                    "base_amount":5
                    ,"available":True,
                    "error_message":"",
                    "price_excl_tax":5,
                    "price_incl_tax":5
                }
            ]
        }
        return simple_response(data)

    @http.route('/api/cart/payment-methods', methods=['GET'], type='http', auth='none', csrf=False)
    def payment_methods(self, **payload):

        data = {
            "code":200,
            "result":
                [
                    {
                        "code":"cashondelivery",
                        "title":"Cash On Delivery"
                    },
                    {
                        "code":"checkmo","title":
                        "Check / Money order"
                    },
                    {
                        "code":"free",
                        "title":"No Payment Information Required"
                    }
                ]
        }
        return simple_response(data)

    @http.route('/api/cart/shipping-information', methods=['OPTIONS'], type='http', auth='none', csrf=False)
    def shipping_information_options(self, **payload):
        data = {
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )

    @http.route('/api/cart/shipping-information', methods=['POST'], type='http', auth='none', csrf=False)
    def shipping_information(self, **payload):

        body = request.httprequest.get_data()
        body_json = json.loads(body.decode("utf-8"))

        data = {
          "code": 200,
          "result": {
            "payment_methods": [
              {
                "code": "cashondelivery",
                "title": "Cash On Delivery"
              },
              {
                "code": "checkmo",
                "title": "Check / Money order"
              }
            ],
            "totals": {
              "grand_total": 45.8,
              "base_grand_total": 55.18,
              "subtotal": 48,
              "base_subtotal": 48,
              "discount_amount": -8.86,
              "base_discount_amount": -8.86,
              "subtotal_with_discount": 39.14,
              "base_subtotal_with_discount": 39.14,
              "shipping_amount": 5,
              "base_shipping_amount": 5,
              "shipping_discount_amount": 0,
              "base_shipping_discount_amount": 0,
              "tax_amount": 9.38,
              "base_tax_amount": 9.38,
              "weee_tax_applied_amount": None,
              "shipping_tax_amount": 0,
              "base_shipping_tax_amount": 0,
              "subtotal_incl_tax": 59.04,
              "shipping_incl_tax": 5,
              "base_shipping_incl_tax": 5,
              "base_currency_code": "USD",
              "quote_currency_code": "USD",
              "items_qty": 2,
              "items": [
                {
                  "item_id": 5853,
                  "price": 24,
                  "base_price": 24,
                  "qty": 2,
                  "row_total": 48,
                  "base_row_total": 48,
                  "row_total_with_discount": 0,
                  "tax_amount": 9.38,
                  "base_tax_amount": 9.38,
                  "tax_percent": 23,
                  "discount_amount": 8.86,
                  "base_discount_amount": 8.86,
                  "discount_percent": 15,
                  "price_incl_tax": 29.52,
                  "base_price_incl_tax": 29.52,
                  "row_total_incl_tax": 59.04,
                  "base_row_total_incl_tax": 59.04,
                  "options": "[]",
                  "weee_tax_applied_amount": None,
                  "weee_tax_applied": None,
                  "name": "Logan  HeatTec&reg; Tee-XS-Black"
                }
              ],
              "total_segments": [
                {
                  "code": "subtotal",
                  "title": "Subtotal",
                  "value": 59.04
                },
                {
                  "code": "shipping",
                  "title": "Shipping & Handling (Flat Rate - Fixed)",
                  "value": 5
                },
                {
                  "code": "discount",
                  "title": "Discount",
                  "value": -8.86
                },
                {
                  "code": "tax",
                  "title": "Tax",
                  "value": 9.38,
                  "area": "taxes",
                  "extension_attributes": {
                    "tax_grandtotal_details": [
                      {
                        "amount": 9.38,
                        "rates": [
                          {
                            "percent": "23",
                            "title": "VAT23"
                          }
                        ],
                        "group_id": 1
                      }
                    ]
                  }
                },
                {
                  "code": "grand_total",
                  "title": "Grand Total",
                  "value": 55.18,
                  "area": "footer"
                }
              ]
            }
          }
        }
        return simple_response(data)

    @http.route('/api/cart/collect-totals', methods=['OPTIONS'], type='http', auth='none', csrf=False)
    def collect_totals_options(self, **payload):
        data = {
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )

    @http.route('/api/cart/collect-totals', methods=['POST'], type='http', auth='none', csrf=False)
    def collect_totals(self, **payload):

        body = request.httprequest.get_data()
        body_json = json.loads(body.decode("utf-8"))

        data = {
          "code": 200,
          "result": {
            "grand_total": 45.8,
            "base_grand_total": 55.18,
            "subtotal": 48,
            "base_subtotal": 48,
            "discount_amount": -8.86,
            "base_discount_amount": -8.86,
            "subtotal_with_discount": 39.14,
            "base_subtotal_with_discount": 39.14,
            "shipping_amount": 5,
            "base_shipping_amount": 5,
            "shipping_discount_amount": 0,
            "base_shipping_discount_amount": 0,
            "tax_amount": 9.38,
            "base_tax_amount": 9.38,
            "weee_tax_applied_amount": None,
            "shipping_tax_amount": 0,
            "base_shipping_tax_amount": 0,
            "subtotal_incl_tax": 59.04,
            "base_subtotal_incl_tax": 59.04,
            "shipping_incl_tax": 5,
            "base_shipping_incl_tax": 5,
            "base_currency_code": "USD",
            "quote_currency_code": "USD",
            "items_qty": 2,
            "items": [
              {
                "item_id": 5853,
                "price": 24,
                "base_price": 24,
                "qty": 2,
                "row_total": 48,
                "base_row_total": 48,
                "row_total_with_discount": 0,
                "tax_amount": 9.38,
                "base_tax_amount": 9.38,
                "tax_percent": 23,
                "discount_amount": 8.86,
                "base_discount_amount": 8.86,
                "discount_percent": 15,
                "price_incl_tax": 29.52,
                "base_price_incl_tax": 29.52,
                "row_total_incl_tax": 59.04,
                "base_row_total_incl_tax": 59.04,
                "options": "[]",
                "weee_tax_applied_amount": None,
                "weee_tax_applied": None,
                "name": "Logan  HeatTec&reg; Tee-XS-Black"
              }
            ],
            "total_segments": [
              {
                "code": "subtotal",
                "title": "Subtotal",
                "value": 59.04
              },
              {
                "code": "shipping",
                "title": "Shipping & Handling (Flat Rate - Fixed)",
                "value": 5
              },
              {
                "code": "discount",
                "title": "Discount",
                "value": -8.86
              },
              {
                "code": "tax",
                "title": "Tax",
                "value": 9.38,
                "area": "taxes",
                "extension_attributes": {
                  "tax_grandtotal_details": [
                    {
                      "amount": 9.38,
                      "rates": [
                        {
                          "percent": "23",
                          "title": "VAT23"
                        }
                      ],
                      "group_id": 1
                    }
                  ]
                }
              },
              {
                "code": "grand_total",
                "title": "Grand Total",
                "value": 55.18,
                "area": "footer"
              }
            ]
          }
        }
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ],
            response=data
        )
