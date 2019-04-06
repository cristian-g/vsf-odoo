import functools
import logging
import json
import werkzeug.wrappers
from odoo import http
from odoo.http import request
from odoo.addons.restful.common import valid_response, invalid_response, extract_arguments, simple_response

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


_routes = [
    '/api/<model>',
    '/api/<model>/<id>',
    '/api/<model>/<id>/<action>'
]


class APIController(http.Controller):
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
    def profile(self, model=None, id=None, **payload):

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

        """
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[('Cache-Control', 'no-store'),
                     ('Pragma', 'no-cache')],
            response=json.dumps({
                'request.httprequest.headers.get': request.httprequest.headers.get('access_token'),
                'request.session.uid': request.session.uid,
                'request.uid': request.uid,
            }),
        )
        """

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

    @validate_token
    @http.route('/api/cart/pull', type='http', auth="none", methods=['GET'], csrf=False)
    def cart(self, **payload):
        user_data = request.env['res.users'].sudo().search_read(
            domain=[('id', '=', request.session.uid)],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )
        data = request.env['sale.order'].sudo().search_read(
            domain=[
                ('partner_id', '=', user_data[0].get('partner_id')[0]),
                ('state', '=', 'draft'),
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
            limit=1,
            order='create_date DESC'
        )
        if data:
            data[0]['lines'] = request.env['sale.order.line'].sudo().search_read(
                domain=[('order_id', '=', data[0]['id'])],
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
            items.append(self.cart_item_json(93, "color", "Color"))
            items.append(self.cart_item_json(142, "size", "Size"))

            return simple_response(
                {
                    "code": 200,
                    "result": items
                }
            )
        else:
            return invalid_response(data)

    def cart_item_json(self, name, item_id):
        return {
          "item_id": 66266,
          "sku": "WS08-XS-Red",
          "qty": 1,
          "name": "Minerva LumaTech&trade; V-Tee",
          "price": 32,
          "product_type": "configurable",
          "quote_id": "dceac8e2172a1ff0cfba24d757653257",
          "product_option": {
            "extension_attributes": {
              "configurable_item_options": [
                {
                  "option_id": "93",
                  "option_value": 58
                },
                {
                  "option_id": "142",
                  "option_value": 167
                }
              ]
            }
          }
        }

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

    @validate_token
    @http.route('/api/edit_quantity', type='http', auth="none", methods=['PATCH'], csrf=False)
    def edit_quantity(self, **payload):

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

        request.env['sale.order.line'].sudo().search([('id', '=', payload.get('line_id'))]).write({
            'product_uom_qty': payload.get('quantity'),
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

    @validate_token
    @http.route('/api/add_to_cart', methods=['POST'], type='http', auth='none', csrf=False)
    def add_to_cart(self, **payload):

        user_data = request.env['res.users'].sudo().search_read(
            domain=[('id', '=', request.session.uid)],
            fields=['partner_id'],
            offset=None,
            limit=1,
            order=None
        )
        order = request.env['sale.order'].sudo().search_read(
            domain=[('partner_id', '=', user_data[0].get('partner_id')[0])],
            fields=['id'],
            offset=None,
            limit=1,
            order='create_date DESC'
        )
        resource = request.env['sale.order.line'].sudo().create({
            'order_id': int(order[0].get('id')),
            'product_id': int(payload.get('product_id')),
            'product_uom_qty': payload.get('quantity'),
            'customer_lead': 0.0,
            'name': 'New line',
            'price_unit': 100.0,
        })
        data = {'id': resource.id}
        if resource:
            return valid_response(data)
        else:
            return invalid_response(data)

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

        data = {
            "code":200,
            "result":"OK"
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

    @validate_token
    @http.route(_routes, type='http', auth="none", methods=['POST'], csrf=False)
    def create(self, model=None, id=None, **payload):
        ioc_name = model
        model = request.env[self._model].sudo().search(
            [('model', '=', model)], limit=1)
        if model:
            try:
                resource = request.env[model.model].sudo().create(payload)
            except Exception as e:
                return invalid_response('params', e)
            else:
                data = {'id': resource.id}
                if resource:
                    return valid_response(data)
                else:
                    return valid_response(data)
        return invalid_response('invalid object model', 'The model %s is not available in the registry.' % ioc_name)

    @validate_token
    @http.route(_routes, type='http', auth="none", methods=['PUT'], csrf=False)
    def put(self, model=None, id=None, **payload):
        """."""
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response('invalid object id', 'invalid literal %s for id with base ' % id)
        _model = request.env[self._model].sudo().search(
            [('model', '=', model)], limit=1)
        if not _model:
            return invalid_response('invalid object model', 'The model %s is not available in the registry.' % model, 404)
        try:
            request.env[_model.model].sudo().browse(_id).write(payload)
        except Exception as e:
            return invalid_response('exception', e.name)
        else:
            return valid_response('update %s record with id %s successfully!' % (_model.model, _id))

    @validate_token
    @http.route(_routes, type='http', auth="none", methods=['DELETE'], csrf=False)
    def delete(self, model=None, id=None, **payload):
        """."""
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response('invalid object id', 'invalid literal %s for id with base ' % id)
        try:
            record = request.env[model].sudo().search([('id', '=', _id)])
            if record:
                record.unlink()
            else:
                return invalid_response('missing_record', 'record object with id %s could not be found' % _id, 404)
        except Exception as e:
            return invalid_response('exception', e.name, 503)
        else:
            return valid_response('record %s has been successfully deleted' % record.id)

    @validate_token
    @http.route(_routes, type='http', auth="none", methods=['PATCH'], csrf=False)
    def patch(self, model=None, id=None, action=None, **payload):
        """."""
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response('invalid object id', 'invalid literal %s for id with base ' % id)
        try:
            record = request.env[model].sudo().search([('id', '=', _id)])
            _callable = action in [method for method in dir(
                record) if callable(getattr(record, method))]
            if record and _callable:
                # action is a dynamic variable.
                getattr(record, action)()
            else:
                return invalid_response('missing_record',
                                        'record object with id %s could not be found or %s object has no method %s' % (_id, model, action), 404)
        except Exception as e:
            return invalid_response('exception', e, 503)
        else:
            return valid_response('record %s has been successfully patched' % record.id)
