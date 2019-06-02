import logging
import json
import werkzeug.wrappers
from odoo import http
from odoo.http import request
from odoo.addons.restful.common import invalid_response, valid_response, simple_response

_logger = logging.getLogger(__name__)

class PublicAPI(http.Controller):
    """."""

    category_offset = 2
    size_attribute_name = "Talla"
    color_attribute_name = "Color"

    def __init__(self):
        return

    @http.route('/api/catalog/vue_storefront_catalog/product/_search', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
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
            domain=[], fields=['id', 'name', 'description', 'price', 'public_categ_ids', 'default_code', 'attribute_line_ids'], offset=None, limit=None,
            order=None)
        if data:
            #return valid_response(self.productJSON())
            products = []
            for element in data:

                # Preparing data for "configurable_options"
                variants_array = []
                attribute_line_ids = element.get('attribute_line_ids')
                for attribute_line_id in attribute_line_ids:
                    variant = request.env['product.template.attribute.line'].sudo().search_read(
                        domain=[('id', '=', attribute_line_id)],
                        fields=['id', 'value_ids', 'attribute_id'],
                        offset=None,
                        limit=None,
                        order=None)[0]
                    value_ids = variant['value_ids']
                    variant['attributes'] = []
                    for value_id in value_ids:
                        attribute = request.env['product.attribute.value'].sudo().search_read(
                            domain=[('id', '=', value_id)],
                            fields=['name', 'html_color'],
                            offset=None,
                            limit=None,
                            order=None)
                        variant['attributes'].append(attribute)
                    variants_array.append(variant)

                # Preparing data for "configurable_children"
                # "product.attribute.value.product.product.rel" relates products with attribute values
                # find products for current template
                configurable_childrens = request.env['product.product'].sudo().search_read(
                domain=[('product_tmpl_id', '=', element.get('id'))],
                fields=['id', 'attribute_value_ids'],
                offset=None,
                limit=None,
                order=None)
                configurable_children_array = []
                for configurable_children in configurable_childrens:

                    configurable_children['attributes'] = []

                    value_ids = configurable_children['attribute_value_ids']
                    for value_id in value_ids:
                        attribute = request.env['product.attribute.value'].sudo().search_read(
                            domain=[('id', '=', value_id)],
                            fields=['id', 'name', 'attribute_id'],
                            offset=None,
                            limit=None,
                            order=None)
                        configurable_children['attributes'].append(attribute)

                    configurable_children_array.append(
                        configurable_children
                    )

                products.append(self.productJSON(
                    element.get('name'),
                    element.get('id'),
                    element.get('default_code'),
                    element.get('attribute_line_ids'),
                    variants_array,
                    configurable_children_array,
                ))
            return valid_response(products)
        else:
            return invalid_response(data)

    def configurable_option_JSON(self, variant, item_id):

        attribute_id = variant.get("attribute_id")[0]
        attribute_name = variant.get("attribute_id")[1]

        attribute_label_json = None
        attribute_code_json = None

        if attribute_name == self.size_attribute_name:
            attribute_label_json = "Size"
            attribute_code_json = "size"
        elif attribute_name == self.color_attribute_name:
            attribute_label_json = "Color"
            attribute_code_json = "color"

        values_array = []
        attributes = variant.get("attributes")
        for attribute in attributes:

            if attribute_name == self.size_attribute_name:
                values_array.append({
                    "value_index": attribute[0].get("id"),
                    "label": str(attribute[0].get("name")),
                })
            elif attribute_name == self.color_attribute_name:
                values_array.append({
                    "value_index": attribute[0].get("id"),
                    "label": "#" + str(attribute[0].get("html_color")),
                })

        result = {
             "attribute_id": attribute_id,
             "values": values_array,
             "product_id": item_id,
             "id": attribute_id,
             "label": attribute_label_json,
             "position": 0,
             "attribute_code": attribute_code_json
          }
        return result

    def configurable_children_JSON(self, configurable, item_id):

        # Get size and color
        size_id = None
        color_id = None
        attributes = configurable.get("attributes")
        for attribute in attributes:

            attribute_name = attribute[0].get("attribute_id")[1]

            if attribute_name == self.size_attribute_name:
                size_id = attribute[0].get("id")
            elif attribute_name == self.color_attribute_name:
                color_id = attribute[0].get("id")

        size_id_string = str(size_id)
        color_id_string = str(color_id)

        result = {
             "image":"/w/s/ws06-yellow_main.jpg",
             "thumbnail":"/w/s/ws06-yellow_main.jpg",
             "color": color_id_string,
             "small_image":"/w/s/ws06-yellow_main.jpg",
             "tax_class_id":"2",
             "has_options":"0",
             "url_key":"elisa-evercool-trade-tee-xl-yellow",
             "regular_price":35.670001,
             "required_options":"0",
             "max_price":35.670001,
             "minimal_regular_price":35.670001,
             "size": size_id_string,
             "final_price":35.670001,
             "special_price":0,
             "price":29,
             "minimal_price":35.670001,
             "name": size_id_string + "-" + color_id_string,
             "id": configurable.get("id"),
             "category_ids":[
                "25",
                "33",
                "8",
                "36",
                "2"
             ],
             # "sku":"WS06-XL-Yellow",
             "sku":"WS06-" + size_id_string + "-" + color_id_string,
             "max_regular_price":35.670001,
             "status":1,
             "priceTax":6.67,
             "priceInclTax":35.67,
             "specialPriceTax": None,
             "specialPriceInclTax": None
          }
        return result

    def productJSON(self, name, item_id, code, attribute_line_ids, variants, configurable_children):

        # Configurable options
        configurable_options_array = []
        for variant in variants:
            configurable_options_array.append(
                self.configurable_option_JSON(variant, item_id)
            )

        # Configurable children
        configurable_children_array = []
        for configurable in configurable_children:
            configurable_children_array.append(
                self.configurable_children_JSON(configurable, item_id)
            )

        source = {
            "attribute_line_ids": attribute_line_ids,
            "variants": variants,
            "configurable_children_array": configurable_children_array,




       "pattern":"197",
       "description":"<p>When rising temps threaten to melt you down, Elisa EverCool™ Tee brings serious relief. Moisture-wicking fabric pulls sweat away from your skin, while the innovative seams hug your muscles to enhance your range of motion.</p>\n<p>• Purple heather v-neck tee.<br />• Short-Sleeves.<br />• Luma EverCool™ fabric. <br />• Machine wash/line dry.</p>",
       "eco_collection":"1",



            # START OF CONFIGURABLE OPTIONS
       "configurable_options_original": variants,
       "configurable_options": configurable_options_array,

            # END OF CONFIGURABLE OPTIONS

            "tsk":1551705236617,
       "custom_attributes": None,
       "size_options":[
          167,
          168,
          169,
          170,
          171
       ],
       "regular_price":29,
       "erin_recommends":"0",
       "final_price":35.670001,
       "price":29,
       "color_options":[
          52,
          57,
          58,
          59
       ],
       "links":{

       },
       "id": item_id,
       "category_ids":[
          "25",
          "33",
          "8",
          "36",
          "2"
       ],
       "sku": str(item_id),
       "stock":{
          "min_sale_qty":1,
          "item_id":item_id,
          "min_qty":0,
          "stock_status_changed_auto":0,
          "is_in_stock":True,
          "max_sale_qty":10000,
          "show_default_notification_message":False,
          "backorders":0,
          "product_id":item_id,
          "qty":0,
          "is_decimal_divided":False,
          "is_qty_decimal":False,
          "low_stock_date": None,
          "use_config_qty_increments":True
       },
#       "slug":"elisa-evercool-and-trade-tee-1465",
#       "url_path":"women/tops-women/tees-women/tees-25/elisa-evercool-and-trade-tee-1465.html",
       "slug": code,
       "url_path": code,
       "image":"/w/s/ws06-purple_main.jpg",
       "new":"1",
       "thumbnail":"/w/s/ws06-purple_main.jpg",
       "visibility":4,
       "type_id":"configurable",
       "tax_class_id":"2",
       "media_gallery":[
          {
             "vid": None,
             "image":"/w/s/ws06-purple_main.jpg",
             "pos":1,
             "typ":"image",
             "lab":""
          },
          {
             "vid": None,
             "image":"/w/s/ws06-purple_back.jpg",
             "pos":2,
             "typ":"image",
             "lab":""
          }
       ],
       "climate":"205,209",
       "style_general":"136",
       "url_key":"elisa-evercool-trade-tee",
       "performance_fabric":"0",
       "sale":"0",
       "max_price":35.670001,
       "minimal_regular_price":35.670001,
       "material":"153,154",
       "special_price":0,
       "minimal_price":35.670001,
       "name": name,

            # START OF CONFIGURABLE CHILDREN

            "configurable_children_original": configurable_children,
            "configurable_children": configurable_children_array,

            # END OF CONFIGURABLE CHILDREN

            "max_regular_price":35.670001,
       "category":[
          {
             "path":"women/tops-women/tees-women/tees-25",
             "category_id":25,
             "name":"Tees",
             "slug":"tees-25"
          },
          {
             "path":"promotions/tees-all/tees-33",
             "category_id":33,
             "name":"Tees",
             "slug":"tees-33"
          },
          {
             "path":"collections/yoga-new/new-luma-yoga-collection-8",
             "category_id":8,
             "name":"New Luma Yoga Collection",
             "slug":"new-luma-yoga-collection-8"
          },
          {
             "path":"collections/eco-friendly/eco-friendly-36",
             "category_id":36,
             "name":"Eco Friendly",
             "slug":"eco-friendly-36"
          },
          {
             "path":"default-category-2",
             "category_id":2,
             "name":"Default Category",
             "slug":"default-category-2"
          }
       ],
       "status":1,
       "priceTax":6.67,
       "priceInclTax":35.67,
       "specialPriceTax": None,
       "specialPriceInclTax": None
    }
        return {
            "_source": source,
            "_score": 1
        }

    @http.route('/api/catalog/vue_storefront_catalog/attribute/_search', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
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

    @http.route('/api/catalog/vue_storefront_catalog/category/_search', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
    def categories(self, **payload):

        #str(json.loads(payload.get('request')).get('_appliedFilters')[0].get('value').get('eq'))
        # == 2 --> root categories

        applied_filter = json.loads(payload.get('request')).get('_appliedFilters')[0]
        if applied_filter.get('attribute') == "url_key":
            parent_id = 2
        else:
            parent_id = applied_filter.get('value').get('eq')

        if parent_id == 2:
            # Root categories
            categories = request.env['product.public.category'].sudo().search_read(
                domain=[('parent_id', '=', False)],
                fields=['id', 'name', 'display_name', 'parent_id', 'child_id'],
                offset=None, limit=None,
                order=None)
            if categories:
                response = self.categories_to_response(categories, 2, parent_id)
                return simple_response(response)
            else:
                return invalid_response({
                    "error": 500
                })
        else:
            categories = request.env['product.public.category'].sudo().search_read(
                domain=[('parent_id', '=', parent_id - self.category_offset)],
                fields=['id', 'name', 'display_name', 'parent_id', 'child_id'],
                offset=None, limit=None,
                order=None)
            if categories:
                response = self.categories_to_response(categories, 3, parent_id)
                return simple_response(response)
            else:
                return invalid_response({
                    "error": 500
                })

            response = {
                "took":1,
                "timed_out": False,
                "_shards":{
                    "total":5,
                    "successful":5,
                    "skipped":0,
                    "failed":0
                },
                "hits":{
                    "total":2,
                    "max_score": None,
                    "hits":[
                        {
                            "_index":"vue_storefront_catalog_1552559102",
                            "_type":"category",
                            "_id":"21",
                            "_score": None,
                            "_source":{
                                "path":"1/2/20/21",
                                "is_active": True,
                                "level":3,
                                "product_count":0,
                                "children_count":"4",
                                "parent_id": parent_id,
                                "name":"Tops" + str(json.loads(payload.get('request')).get('_appliedFilters')[0].get('value').get('eq')),
                                "id":21,
                                "url_path":"women/tops-women/tops-21",
                                "url_key":"tops-21",
                                "children_data":[
                                    {
                                        "id":23
                                    },
                                    {
                                        "id":24
                                    },
                                    {
                                        "id":25
                                    },
                                    {
                                        "id":26
                                    }
                                ]
                            },
                            "sort":[
                                1
                            ]
                        },
                        {
                            "_index":"vue_storefront_catalog_1552559102",
                            "_type":"category",
                            "_id":"22",
                            "_score": None,
                            "_source":{
                                "path":"1/2/20/22",
                                "is_active": True,
                                "level":3,
                                "product_count":0,
                                "children_count":"2",
                                "parent_id": parent_id,
                                "name":"Bottoms",
                                "id":22,
                                "url_key":"bottoms-22",
                                "children_data":[
                                    {
                                        "id":27
                                    },
                                    {
                                        "id":28
                                    }
                                ],
                                "url_path":"women/bottoms-women/bottoms-22"
                            },
                            "sort":[
                                2
                            ]
                        }
                    ]
                }
            }
            return simple_response(response)


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
            domain=[('parent_id', '=', False)],
            fields=['id', 'name', 'display_name', 'parent_id', 'child_id'],
            offset=None, limit=None,
            order=None)
        if data:
            return valid_response(data)
        else:
            return invalid_response(data)

    def categories_to_response(self, categories, level, parent_id):
        categories_array = []
        for category in categories:
            categories_array.append(self.category_json(
                category["name"],
                category["id"],
                parent_id,
                category["child_id"],
                level
            ))

        response = {
            "took": 1,
            "timed_out": False,
            "_shards": {
                "total": 5,
                "successful": 5,
                "skipped": 0,
                "failed": 0
            },
            "hits": {
                "total": 6,
                "max_score": None,
                "hits": categories_array
            }
        }
        return response

    def category_json(self, name, id, parent_id, childs, level):
        children_data = []
        for child in childs:
            children_data.append({
                "id": child
            })
        result = {
                        "_index":"vue_storefront_catalog_1552559102",
                        "_type":"category",
                        "_id": id,
                        "_score": None,
                        "_source":{
                            "path":"1/2/20",
                            "is_active": True,
                            "level": level,
                            "product_count":1,
                            "children_count": len(children_data),
                            "parent_id": parent_id,
                            "name": name,
                            "id": id + self.category_offset,
                            "url_path":"women/women-20",
                            "url_key":"women-20",
                            "children_data": children_data
                        },
                        "sort":[
                            2
                        ]
                    }
        return result

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
