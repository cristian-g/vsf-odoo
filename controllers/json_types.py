class JsonTypes():

    @staticmethod
    def productJSON(name, item_id, code, price, attribute_line_ids, variants, configurable_children, size_attribute_name, color_attribute_name, host_odoo):

        # Configurable options
        configurable_options_array = []
        for variant in variants:
            configurable_options_array.append(
                JsonTypes.configurable_option_JSON(
                    variant,
                    item_id,
                    size_attribute_name,
                    color_attribute_name
                )
            )

        # Configurable children
        configurable_children_array = []
        for configurable in configurable_children:
            configurable_children_array.append(
                JsonTypes.configurable_children_JSON(
                    configurable,
                    item_id,
                    size_attribute_name,
                    color_attribute_name,
                    host_odoo
                )
            )

        # First variant id
        first_variant_id = configurable_children[0].get("id")

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
       "final_price": price,
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
       # "image":"/w/s/ws06-purple_main.jpg",
       "image": host_odoo + "/web/image/product.product/" + str(first_variant_id) + "/image",
       "new":"1",
       "thumbnail": host_odoo + "/web/image/product.product/" + str(first_variant_id) + "/image",
       "visibility":4,
       "type_id":"configurable",
       "tax_class_id":"2",
       "media_gallery": [],
       "climate":"205,209",
       "style_general":"136",
       "url_key":"elisa-evercool-trade-tee",
       "performance_fabric":"0",
       "sale":"0",
       "max_price": price,
       "minimal_regular_price": price,
       "material":"153,154",
       "special_price":0,
       "minimal_price": price,
       "name": name,

            # START OF CONFIGURABLE CHILDREN

            "configurable_children_original": configurable_children,
            "configurable_children": configurable_children_array,

            # END OF CONFIGURABLE CHILDREN

            "max_regular_price": price,
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
       "priceInclTax": price,
       "specialPriceTax": None,
       "specialPriceInclTax": None
    }
        return {
            "_source": source,
            "_score": 1
        }

    @staticmethod
    def configurable_option_JSON(variant, item_id, size_attribute_name, color_attribute_name):

        attribute_id = variant.get("attribute_id")[0]
        attribute_name = variant.get("attribute_id")[1]

        attribute_label_json = None
        attribute_code_json = None

        if attribute_name == size_attribute_name:
            attribute_label_json = "Size"
            attribute_code_json = "size"
        elif attribute_name == color_attribute_name:
            attribute_label_json = "Color"
            attribute_code_json = "color"

        values_array = []
        attributes = variant.get("attributes")
        for attribute in attributes:

            if attribute_name == size_attribute_name:
                values_array.append({
                    "value_index": attribute[0].get("id"),
                    "label": str(attribute[0].get("name")),
                })
            elif attribute_name == color_attribute_name:
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

    @staticmethod
    def configurable_children_JSON(configurable, item_id, size_attribute_name, color_attribute_name, host_odoo):

        # Get size and color
        size_id = None
        color_id = None
        attributes = configurable.get("attributes")
        for attribute in attributes:

            attribute_name = attribute[0].get("attribute_id")[1]

            if attribute_name == size_attribute_name:
                size_id = attribute[0].get("id")
            elif attribute_name == color_attribute_name:
                color_id = attribute[0].get("id")

        size_id_string = str(size_id)
        color_id_string = str(color_id)

        result = {
             "image": host_odoo + "/web/image/product.product/" + str(configurable.get("id")) + "/image",
             "thumbnail": host_odoo + "/web/image/product.product/" + str(configurable.get("id")) + "/image",
             "color": color_id_string,
             "small_image": host_odoo + "/web/image/product.product/" + str(configurable.get("id")) + "/image",
             "tax_class_id":"2",
             "has_options":"0",
             "url_key":"elisa-evercool-trade-tee-xl-yellow",
             "regular_price": configurable.get("list_price"),
             "required_options":"0",
             "max_price": configurable.get("list_price"),
             "minimal_regular_price": configurable.get("list_price"),
             "size": size_id_string,
             "final_price": configurable.get("list_price"),
             "special_price":0,
             "price":29,
             "minimal_price": configurable.get("list_price"),
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
             # "sku":"WS06-" + size_id_string + "-" + color_id_string,
             "sku": str(configurable.get("id")),
             "max_regular_price": configurable.get("list_price"),
             "status":1,
             "priceTax":6.67,
             "priceInclTax": configurable.get("list_price"),
             "specialPriceTax": None,
             "specialPriceInclTax": None
          }
        return result

    @staticmethod
    def attributeJSON(attribute_id, attribute_code, default_frontend_label):
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

    @staticmethod
    def category_json(name, id, parent_id, childs, level, category_offset):
        children_data = []
        for child in childs:
            children_data.append({
                "id": child
            })
        children_count = len(children_data)

        if children_count == 0:
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
                                "children_count": str(children_count),
                                "parent_id": parent_id,
                                "name": name,
                                "id": id + category_offset,
                                "url_path": "categories/category-" + str(id + category_offset),
                                "url_key": str(id + category_offset),
                            },
                            "sort":[
                                2
                            ]
                        }
        else:
            result = {
                "_index": "vue_storefront_catalog_1552559102",
                "_type": "category",
                "_id": id,
                "_score": None,
                "_source": {
                    "path": "1/2/20",
                    "is_active": True,
                    "level": level,
                    "product_count": 1,
                    "children_count": str(children_count),
                    "parent_id": parent_id,
                    "name": name,
                    "id": id + category_offset,
                    "url_path": "categories/category-" + str(id + category_offset),
                    "url_key": str(id + category_offset),
                    "children_data": children_data
                },
                "sort": [
                    2
                ]
            }
        return result

    @staticmethod
    def categories_to_response(categories, level, parent_id, category_offset):
        categories_array = []
        for category in categories:
            categories_array.append(JsonTypes.category_json(
                category["name"],
                category["id"],
                parent_id,
                category["child_id"],
                level,
                category_offset
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