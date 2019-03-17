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
                products.append(self.productJSON(element.get('name')))
            return valid_response(products)
        else:
            return invalid_response(data)

    def productJSON(self, name):
        return {
              "pattern":"197",
              "slug":"slug",
              "description":"<p>Stay comfortable and stay in the race no matter what the weather's up to. The Bruno Compete Hoodie's water-repellent exterior shields you from the elements, while advanced fabric technology inside wicks moisture to keep you dry.<\/p>\n<p>\u2022 Full zip black hoodie pullover. <br \/>\u2022 Adjustable drawstring hood. <br \/>\u2022 Ribbed cuffs\/waistband. <br \/>\u2022 Kangaroo pocket. <br \/>\u2022 Machine wash\/dry.<\/p>",
              "eco_collection":"1",
              "configurable_options":[
                 {
                    "attribute_id":"93",
                    "values":[
                       {
                          "value_index":49,
                          "label":"Black"
                       },
                       {
                          "value_index":50,
                          "label":"Blue"
                       },
                       {
                          "value_index":53,
                          "label":"Green"
                       }
                    ],
                    "product_id":99,
                    "id":7,
                    "label":"Color",
                    "slug":"slug",
                    "position":1,
                    "attribute_code":"color"
                 },
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
                    "product_id":99,
                    "id":6,
                    "label":"Size",
                    "slug":"slug",
                    "position":0,
                    "attribute_code":"size"
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
              "id":99,
              "category_ids":[
                 "15",
                 "36",
                 "2"
              ],
              "sku":"MH03",
              "stock":{
                 "min_sale_qty":1,
                 "item_id":99,
                 "min_qty":0,
                 "stock_status_changed_auto":0,
                 "is_in_stock":True,
                 "max_sale_qty":10000,
                 "show_default_notification_message":False,
                 "backorders":0,
                 "product_id":99,
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
              "configurable_children":[

              ],
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

    @http.route('/api/catalog/vue_storefront_catalog/category', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
    def categories(self, **payload):
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
