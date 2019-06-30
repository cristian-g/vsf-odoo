import logging
import json
import werkzeug.wrappers
from odoo import http
from odoo.http import request
from odoo.addons.vue_storefront.common import invalid_response, valid_response, simple_response
from odoo.addons.vue_storefront.controllers.json_types import JSONTypes

_logger = logging.getLogger(__name__)

class PublicAPIController(http.Controller):
    """."""

    def __init__(self):
        self.host_odoo = str(request.env.ref('vue_storefront.host_odoo').sudo().value)
        self.category_offset = int(request.env.ref('vue_storefront.category_offset').sudo().value)
        self.size_attribute_name = str(request.env.ref('vue_storefront.size_attribute_name').sudo().value)
        self.color_attribute_name = str(request.env.ref('vue_storefront.color_attribute_name').sudo().value)
        return

    @http.route('/api/catalog/vue_storefront_catalog/product/_search', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
    def products(self, **payload):

        # Detect specific category
        requested_id = -1
        applied_filters = json.loads(payload.get('request')).get('_appliedFilters')
        for applied_filter in applied_filters:
            if applied_filter.get('attribute') == "category_ids":
                ins = applied_filter.get('value').get('in')
                if len(ins) == 1:
                    slug = applied_filter.get('value').get('in')[0]
                    requested_id = int(slug.split("-")[-1]) - self.category_offset
        domain = []
        if requested_id != -1:
            domain = [('public_categ_ids', 'in', [requested_id])]

        data = request.env['product.template'].sudo().search_read(
            domain=domain, fields=[
                'id',
                'name',
                'description',
                'list_price',
                'public_categ_ids',
                'default_code',
                'attribute_line_ids'
            ], offset=None, limit=None,
            order=None)
        if data:
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

                    configurable_children['list_price'] = element.get('list_price')
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

                products.append(JSONTypes.productJSON(
                    element.get('name'),
                    element.get('id'),
                    element.get('default_code'),
                    element.get('list_price'),
                    element.get('attribute_line_ids'),
                    variants_array,
                    configurable_children_array,
                    self.size_attribute_name,
                    self.color_attribute_name,
                    self.host_odoo,
                ))
            return valid_response(products)
        else:
            return invalid_response(data)

    @http.route('/api/catalog/vue_storefront_catalog/attribute/_search', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
    def attributes_json(self, **payload):
        attributes = []
        attributes.append(JSONTypes.attributeJSON(
            True,  # is_html_allowed_on_front
            False,  # used_for_sort_by
            False,  # is_used_in_grid
            False,  # is_filterable_in_grid
            [],  # apply_to
            "0",  # is_searchable
            "0",  # is_visible_in_advanced_search
            "1",  # is_used_for_promo_rules
            "0",  # used_in_product_listing
            145,  # attribute_id
            "erin_recommends",  # attribute_code
            "boolean",  # frontend_input
            False,  # is_required
            [
              {
                 "label":"Yes",
                 "value":"1"
              },
              {
                 "label":"No",
                 "value":"0"
              }
            ],  # options
            True,  # is_user_defined
            "Erin Recommends",  # default_frontend_label
            "int",  # backend_type
            "Magento\\Eav\\Model\\Entity\\Attribute\\Source\\Boolean",  # backend_model
            "Magento\\Eav\\Model\\Entity\\Attribute\\Source\\Boolean",  # source_model
            "",  # default_value
            145,  # id
        ))
        attributes.append(JSONTypes.attributeJSON(
            True,  # is_html_allowed_on_front
            False,  # used_for_sort_by
            False,  # is_used_in_grid
            False,  # is_filterable_in_grid
            [],  # apply_to
            "0",  # is_searchable
            "0",  # is_visible_in_advanced_search
            "1",  # is_used_for_promo_rules
            "1",  # used_in_product_listing
            142,  # attribute_id
            "size",  # attribute_code
            "select",  # frontend_input
            False,  # is_required
            [
              {
                 "label":" ",
                 "value":""
              },
              {
                 "label":"55 cm",
                 "value":"91"
              },
              {
                 "label":"XS",
                 "value":"167"
              },
              {
                 "label":"65 cm",
                 "value":"92"
              },
              {
                 "label":"S",
                 "value":"168"
              },
              {
                 "label":"75 cm",
                 "value":"93"
              },
              {
                 "label":"M",
                 "value":"169"
              },
              {
                 "label":"6 foot",
                 "value":"94"
              },
              {
                 "label":"L",
                 "value":"170"
              },
              {
                 "label":"8 foot",
                 "value":"95"
              },
              {
                 "label":"XL",
                 "value":"171"
              },
              {
                 "label":"10 foot",
                 "value":"96"
              },
              {
                 "label":"28",
                 "value":"172"
              },
              {
                 "label":"29",
                 "value":"173"
              },
              {
                 "label":"30",
                 "value":"174"
              },
              {
                 "label":"31",
                 "value":"175"
              },
              {
                 "label":"32",
                 "value":"176"
              },
              {
                 "label":"33",
                 "value":"177"
              },
              {
                 "label":"34",
                 "value":"178"
              },
              {
                 "label":"36",
                 "value":"179"
              },
              {
                 "label":"38",
                 "value":"180"
              }
            ],  # options
            True,  # is_user_defined
            "Talla",  # default_frontend_label
            "int",  # backend_type
            "Magento\\Eav\\Model\\Entity\\Attribute\\Source\\Table",  # backend_model
            "Magento\\Eav\\Model\\Entity\\Attribute\\Source\\Table",  # source_model
            "91",  # default_value
            142,  # id
        ))
        attributes.append(JSONTypes.attributeJSON(
            True,  # is_html_allowed_on_front
            False,  # used_for_sort_by
            True,  # is_used_in_grid
            True,  # is_filterable_in_grid
            [
              "simple",
              "virtual",
              "configurable"
            ],  # apply_to
            "0",  # is_searchable
            "0",  # is_visible_in_advanced_search
            "1",  # is_used_for_promo_rules
            "1",  # used_in_product_listing
            93,  # attribute_id
            "color",  # attribute_code
            "select",  # frontend_input
            False,  # is_required
            [
              {
                 "label":" ",
                 "value":""
              },
              {
                 "label":"Black",
                 "value":"49"
              },
              {
                 "label":"Blue",
                 "value":"50"
              },
              {
                 "label":"Brown",
                 "value":"51"
              },
              {
                 "label":"Gray",
                 "value":"52"
              },
              {
                 "label":"Green",
                 "value":"53"
              },
              {
                 "label":"Lavender",
                 "value":"54"
              },
              {
                 "label":"Multi",
                 "value":"55"
              },
              {
                 "label":"Orange",
                 "value":"56"
              },
              {
                 "label":"Purple",
                 "value":"57"
              },
              {
                 "label":"Red",
                 "value":"58"
              },
              {
                 "label":"White",
                 "value":"59"
              },
              {
                 "label":"Yellow",
                 "value":"60"
              }
            ],  # options
            True,  # is_user_defined
            "Color",  # default_frontend_label
            "int",  # backend_type
            "Magento\\Eav\\Model\\Entity\\Attribute\\Source\\Table",  # backend_model
            "Magento\\Eav\\Model\\Entity\\Attribute\\Source\\Table",  # source_model
            "49",  # default_value
            93,  # id
        ))
        attributes.append(JSONTypes.attributeJSON(
            False,  # is_html_allowed_on_front
            True,  # used_for_sort_by
            False,  # is_used_in_grid
            False,  # is_filterable_in_grid
            [
              "simple",
              "virtual",
              "bundle",
              "downloadable",
              "configurable"
            ],  # apply_to
            "1",  # is_searchable
            "1",  # is_visible_in_advanced_search
            "0",  # is_used_for_promo_rules
            "1",  # used_in_product_listing
            77,  # attribute_id
            "price",  # attribute_code
            "price",  # frontend_input
            True,  # is_required
            [],  # options
            False,  # is_user_defined
            "Precio",  # default_frontend_label
            "decimal",  # backend_type
            "Magento\\Catalog\\Model\\Product\\Attribute\\Backend\\Price",  # backend_model
            "Magento\\Catalog\\Model\\Product\\Attribute\\Backend\\Price",  # source_model
            "",  # default_value
            77,  # id
        ))
        return valid_response(attributes)

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

        request_json = json.loads(payload.get('request'))

        # Check if detail of category
        query_json = json.loads(payload.get('request')).get('query')
        if query_json:
            specific_url_key = json.loads(payload.get('request')).get('query').get('bool').get('filter').get('bool').get('must')[0].get('terms').get('url_key')[0]
            int_specific_url_key = int(specific_url_key)
            # Find category
            categories = request.env['product.public.category'].sudo().search_read(
                domain=[('id', '=', int_specific_url_key)],
                fields=['id', 'name', 'display_name', 'parent_id', 'child_id'],
                offset=None, limit=None,
                order=None)
            if categories:
                parent_id = 2
                response = JSONTypes.categories_to_response(categories, 2, parent_id, self.category_offset)
                return simple_response(response)
            else:
                return invalid_response({
                    "error": 500
                })

        applied_filters = json.loads(payload.get('request')).get('_appliedFilters')
        applied_filter = applied_filters[0]

        # Check if detail of category with slug
        if applied_filter.get('attribute') == "slug":
            slug = applied_filter.get('value').get('eq')
            requested_id = int(slug.split("-")[-1]) - self.category_offset
            # Find category
            categories = request.env['product.public.category'].sudo().search_read(
                domain=[('id', '=', requested_id)],
                fields=['id', 'name', 'display_name', 'parent_id', 'child_id'],
                offset=None, limit=None,
                order=None)
            if categories:
                parent_id = 2
                response = JSONTypes.categories_to_response(categories, 2, parent_id, self.category_offset)
                return simple_response(response)
            else:
                return invalid_response({
                    "error": 500
                })

        if applied_filter.get('attribute') == "url_key" or (len(applied_filters) == 1 and applied_filter.get('attribute') == "is_active"):
            parent_id = 2
        else:
            parent_id = applied_filter.get('value').get('eq')

        if parent_id == 2 or parent_id is None:
            # Root categories
            categories = request.env['product.public.category'].sudo().search_read(
                domain=[('parent_id', '=', False)],
                fields=['id', 'name', 'display_name', 'parent_id', 'child_id'],
                offset=None, limit=None,
                order=None)
            if categories:
                response = JSONTypes.categories_to_response(categories, 2, parent_id, self.category_offset)
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
                response = JSONTypes.categories_to_response(categories, 3, parent_id, self.category_offset)
                return simple_response(response)
            else:
                return invalid_response({
                    "error": 500
                })

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

    @http.route('/api/catalog/vue_storefront_catalog/review/_search', type='http', auth="none", methods=['OPTIONS'], csrf=False)
    def reviews_options(self, **payload):
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

    @http.route('/api/catalog/vue_storefront_catalog/review/_search', methods=['GET', 'OPTIONS'], type='http', auth='none', csrf=False)
    def reviews(self, **payload):
        return valid_response([])