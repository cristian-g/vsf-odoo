import logging
import json
import werkzeug.wrappers
from odoo import http
from odoo.http import request
from odoo.addons.restful.common import invalid_response, valid_response, simple_response

_logger = logging.getLogger(__name__)

class PublicAPI(http.Controller):
    """."""

    def __init__(self):
        return

    @http.route('/api/catalog/vue_storefront_catalog/product', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
    def products(self, **payload):
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
            #return valid_response(self.productJSON())
            products = []
            for element in data:
                products.append(self.productJSON(element.get('name'), element.get('id')))
            return valid_response(products)
        else:
            return invalid_response(data)

    def productJSON(self, name, item_id):
        return {
              "pattern":"197",
              "slug":"slug",
              "description":"<p>Stay comfortable and stay in the race no matter what the weather's up to. The Bruno Compete Hoodie's water-repellent exterior shields you from the elements, while advanced fabric technology inside wicks moisture to keep you dry.<\/p>\n<p>\u2022 Full zip black hoodie pullover. <br \/>\u2022 Adjustable drawstring hood. <br \/>\u2022 Ribbed cuffs\/waistband. <br \/>\u2022 Kangaroo pocket. <br \/>\u2022 Machine wash\/dry.<\/p>",
              "eco_collection":"1",
              "configurable_options":[
                 {
                    "attribute_id":"142",
                    "values":[
                       {
                          "value_index":167,
                          "label":"XS"
                       },
                       {
                          "value_index":168,
                          "label":"S"
                       },
                       {
                          "value_index":169,
                          "label":"M"
                       },
                       {
                          "value_index":170,
                          "label":"L"
                       },
                       {
                          "value_index":171,
                          "label":"XL"
                       }
                    ],
                    "product_id": item_id,
                    "id": item_id,
                    "label":"Size",
                    "slug":"slug",
                    "position":0,
                    "attribute_code":"size"
                 },
                 {
                    "attribute_id":"93",
                    "values":[
                       {
                          "value_index":167,
                          "label":"XS"
                       },
                       {
                          "value_index":168,
                          "label":"S"
                       },
                       {
                          "value_index":169,
                          "label":"M"
                       },
                       {
                          "value_index":170,
                          "label":"L"
                       },
                       {
                          "value_index":171,
                          "label":"XL"
                       }
                    ],
                    "product_id": item_id,
                    "id": item_id,
                    "label":"Color",
                    "slug":"slug",
                    "position":0,
                    "attribute_code":"color"
                 }
              ],

                "configurable_children": [
                    {
                        "image": "/w/s/wsh12-green_main.jpg",
                        "color": "53",
                        "size": "172",
                        "special_price": 0,
                        "price": 45,
                        "id": 2030,
                        "sku": "WSH12-28-Green",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-purple_main.jpg",
                        "color": "57",
                        "size": "172",
                        "special_price": 0,
                        "price": 45,
                        "id": 2031,
                        "sku": "WSH12-28-Purple",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-red_main.jpg",
                        "color": "58",
                        "size": "172",
                        "special_price": 0,
                        "price": 45,
                        "id": 2032,
                        "sku": "WSH12-28-Red",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-green_main.jpg",
                        "color": "53",
                        "size": "173",
                        "special_price": 0,
                        "price": 45,
                        "id": 2033,
                        "sku": "WSH12-29-Green",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-purple_main.jpg",
                        "color": "57",
                        "size": "173",
                        "special_price": 0,
                        "price": 45,
                        "id": 2034,
                        "sku": "WSH12-29-Purple",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-red_main.jpg",
                        "color": "58",
                        "size": "173",
                        "special_price": 0,
                        "price": 45,
                        "id": 2035,
                        "sku": "WSH12-29-Red",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-green_main.jpg",
                        "color": "53",
                        "size": "174",
                        "special_price": 0,
                        "price": 45,
                        "id": 2036,
                        "sku": "WSH12-30-Green",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-purple_main.jpg",
                        "color": "57",
                        "size": "174",
                        "special_price": 0,
                        "price": 45,
                        "id": 2037,
                        "sku": "WSH12-30-Purple",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-red_main.jpg",
                        "color": "58",
                        "size": "174",
                        "special_price": 0,
                        "price": 45,
                        "id": 2038,
                        "sku": "WSH12-30-Red",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-green_main.jpg",
                        "color": "53",
                        "size": "175",
                        "special_price": 0,
                        "price": 45,
                        "id": 2039,
                        "sku": "WSH12-31-Green",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-purple_main.jpg",
                        "color": "57",
                        "size": "175",
                        "special_price": 0,
                        "price": 45,
                        "id": 2040,
                        "sku": "WSH12-31-Purple",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-red_main.jpg",
                        "color": "58",
                        "size": "175",
                        "special_price": 0,
                        "price": 45,
                        "id": 2041,
                        "sku": "WSH12-31-Red",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-green_main.jpg",
                        "color": "53",
                        "size": "176",
                        "special_price": 0,
                        "price": 45,
                        "id": 2042,
                        "sku": "WSH12-32-Green",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-purple_main.jpg",
                        "color": "57",
                        "size": "176",
                        "special_price": 0,
                        "price": 45,
                        "id": 2043,
                        "sku": "WSH12-32-Purple",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    },
                    {
                        "image": "/w/s/wsh12-red_main.jpg",
                        "color": "58",
                        "size": "176",
                        "special_price": 0,
                        "price": 45,
                        "id": 2044,
                        "sku": "WSH12-32-Red",
                        "priceTax": 10.35,
                        "priceInclTax": 55.35,
                        "specialPriceTax": None,
                        "specialPriceInclTax": None
                    }
                ],


              "tsk":1549474025451,
              "custom_attributes":None,
              "size_options":[
                 167,
                 168,
                 169,
                 170,
                 171
              ],
              "regular_price":63,
              "final_price":77.490001,
              "erin_recommends":"1",
              "price":63,
              "color_options":[
                 49,
                 50,
                 53
              ],
              "links":[

              ],
              "id": item_id,
              "category_ids":[
                 "15",
                 "36",
                 "2"
              ],
              "sku":"MH" + str(item_id),
              "stock":{
                 "min_sale_qty":1,
                 "item_id": item_id,
                 "min_qty":0,
                 "stock_status_changed_auto":0,
                 "is_in_stock":True,
                 "max_sale_qty":10000,
                 "show_default_notification_message":False,
                 "backorders":0,
                 "product_id": item_id,
                 "qty":0,
                 "is_decimal_divided":False,
                 "is_qty_decimal":False,
                 "low_stock_date":None,
                 "use_config_qty_increments":True
              },
              "image":"\/m\/h\/mh03-black_main.jpg",
              "new":"1",
              "thumbnail":"\/m\/h\/mh03-black_main.jpg",
              "visibility":4,
              "type_id":"configurable",
              "tax_class_id":"2",
              "media_gallery":[
                 {
                    "image":"\/m\/h\/mh03-black_main.jpg",
                    "pos":1,
                    "typ":"image",
                    "lab":""
                 },
                 {
                    "image":"\/m\/h\/mh03-black_alt1.jpg",
                    "pos":2,
                    "typ":"image",
                    "lab":""
                 },
                 {
                    "image":"\/m\/h\/mh03-black_back.jpg",
                    "pos":3,
                    "typ":"image",
                    "lab":""
                 }
              ],
              "climate":"202,204,205,208,210",
              "url_key":"bruno-compete-hoodie",
              "performance_fabric":"0",
              "sale":"0",
              "max_price":77.490001,
              "minimal_regular_price":77.490001,
              "material":"154",
              "special_price":0,
              "minimal_price":77.490001,
              "name":name,
              "max_regular_price":77.490001,
              "category":[
                 {
                    "category_id":15,
                    "name":"Hoodies & Sweatshirts"
                 },
                 {
                    "category_id":36,
                    "name":"Eco Friendly"
                 },
                 {
                    "category_id":2,
                    "name":"Default Category"
                 }
              ],
              "status":1,
              "priceTax":14.49,
              "priceInclTax":77.49,
              "specialPriceTax":None,
              "specialPriceInclTax":None
           }

    @http.route('/api/catalog/vue_storefront_catalog/attribute', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
    def attributes_json(self, **payload):
        attributes = []
        attributes.append(self.attributeJSON("93", "color", "Color"))
        attributes.append(self.attributeJSON("142", "size", "Size"))
        return valid_response(attributes)

    def attributeJSON(self, attribute_id, attribute_code, default_frontend_label):
        return {
          "is_wysiwyg_enabled": False,
          "is_html_allowed_on_front": True,
          "used_for_sort_by": False,
          "is_filterable": True,
          "is_filterable_in_search": False,
          "is_used_in_grid": False,
          "is_visible_in_grid": False,
          "is_filterable_in_grid": False,
          "position": 0,
          "apply_to": [],
          "is_searchable": "0",
          "is_visible_in_advanced_search": "0",
          "is_comparable": "0",
          "is_used_for_promo_rules": "1",
          "is_visible_on_front": "0",
          "used_in_product_listing": "1",
          "is_visible": True,
          "scope": "global",
          "attribute_id": attribute_id,
          "attribute_code": attribute_code,
          "frontend_input": "select",
          "entity_type_id": "4",
          "is_required": False,
          "options": [
            {
              "label": " ",
              "value": ""
            },
            {
              "label": "55 cm",
              "value": "91"
            },
            {
              "label": "XS",
              "value": "167"
            },
            {
              "label": "65 cm",
              "value": "92"
            },
            {
              "label": "S",
              "value": "168"
            },
            {
              "label": "75 cm",
              "value": "93"
            },
            {
              "label": "M",
              "value": "169"
            },
            {
              "label": "6 foot",
              "value": "94"
            },
            {
              "label": "L",
              "value": "170"
            },
            {
              "label": "8 foot",
              "value": "95"
            },
            {
              "label": "XL",
              "value": "171"
            },
            {
              "label": "10 foot",
              "value": "96"
            },
            {
              "label": "28",
              "value": "172"
            },
            {
              "label": "29",
              "value": "173"
            },
            {
              "label": "30",
              "value": "174"
            },
            {
              "label": "31",
              "value": "175"
            },
            {
              "label": "32",
              "value": "176"
            },
            {
              "label": "33",
              "value": "177"
            },
            {
              "label": "34",
              "value": "178"
            },
            {
              "label": "36",
              "value": "179"
            },
            {
              "label": "38",
              "value": "180"
            }
          ],
          "is_user_defined": True,
          "default_frontend_label": default_frontend_label,
          "frontend_labels": None,
          "backend_type": "int",
          "is_unique": "0",
          "validation_rules": [],
          "id": 142,
          "tsk": 1512134647691,
          "default_value": "91",
          "source_model": "Magento\\Eav\\Model\\Entity\\Attribute\\Source\\Table",
          "sgn": "vHkjS2mGumtgjjzlDrGJnF6i8EeUU2twc2zkZe69ABc"
        }

    @http.route('/api/stock/check', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
    def stock_check(self, **payload):
        response = {
            "code": 200,
            "result": {
                "item_id": 580,
                "product_id": 580,
                "stock_id": 1,
                "qty": 53,
                "is_in_stock": True,
                "is_qty_decimal": False,
                "show_default_notification_message": False,
                "use_config_min_qty": True,
                "min_qty": 0,
                "use_config_min_sale_qty": 1,
                "min_sale_qty": 1,
                "use_config_max_sale_qty": True,
                "max_sale_qty": 10000,
                "use_config_backorders": True,
                "backorders": 0,
                "use_config_notify_stock_qty": True,
                "notify_stock_qty": 1,
                "use_config_qty_increments": True,
                "qty_increments": 0,
                "use_config_enable_qty_inc": True,
                "enable_qty_increments": False,
                "use_config_manage_stock": True,
                "manage_stock": True,
                "low_stock_date": None,
                "is_decimal_divided": False,
                "stock_status_changed_auto": 0
            }
        }
        return simple_response(response)

    @http.route('/api/catalog/vue_storefront_catalog/category', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
    def categories(self, **payload):

        response = {
            "items": [
                {
                    "id": 27,
                    "parent_id": 2,
                    "name": "Category without childs",
                    "is_active": True,
                    "position": 5,
                    "level": 2,
                    "product_count": 2,

                    "entity_type_id": 3,
                    "attribute_set_id": 3,
                    "children_count": 0,
                    "request_path": "accessories/shoes.html",


                    "children_data": [

                    ],
                    "created_at": "2017-11-06 12:16:41",
                    "updated_at": "2017-11-06 12:16:42",
                    "path": "1/2/29",
                    "available_sort_by": [

                    ],
                    "include_in_menu": False,
                    "display_mode": "PAGE",
                    "is_anchor": "0",
                    "url_key": "promotions-29",
                    "url_path": "promotions/promotions-29",
                    "slug": "promotions-29",
                    "tsk": 1551705224325
                }
            ],
            "total": 3,
            "start": 1,
            "perPage": 3,
            "aggregations": [

            ]
        }
        return simple_response(response)

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

    @http.route('/api/user/create', type='http', auth="none", methods=['OPTIONS'], csrf=False)
    def signup_options(self, **payload):
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

    @http.route('/api/user/create', methods=['POST'], type='http', auth='none', csrf=False)
    def signup(self, **payload):

        body = request.httprequest.get_data()
        payload = json.loads(body.decode("utf-8"))

        firstname = payload.get('customer').get('firstname')
        lastname = payload.get('customer').get('lastname')
        email = payload.get('customer').get('email')
        password = payload.get('password')

        resource = request.env['res.users'].sudo().create({
                  'name': firstname,
                  'parent_name': lastname,
                  'login': email,
                  'company_ids': [1],
                  'company_id': 1,
                  'new_password': password,
                  'is_company' : False,
                   'groups_id': [9]
              })

        #data = {'id': resource.id}
        data = {
          "code": 200,
          "result": {
            "id": resource.id,
            "group_id": 1,
            "created_at": "2018-04-03 13:35:13",
            "updated_at": "2018-04-03 13:35:13",
            "created_in": "Default Store View",
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            "store_id": 1,
            "website_id": 1,
            "addresses": [],
            "disable_auto_group_change": 0
          }
        }

        request.env.cr.execute('INSERT INTO res_company_users_rel(user_id, cid) VALUES('+str(resource.id)+', 1)')
        if resource:
            return simple_response(data)
        else:
            return invalid_response(data)
