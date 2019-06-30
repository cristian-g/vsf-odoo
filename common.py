import ast
import json
import werkzeug.wrappers

host = "http://localhost:8069"
category_offset = 2
size_attribute_name = "Talla"
color_attribute_name = "Color"

def valid_response(data, status=200):
    """Valid Response
    This will be return when the http request was successfully processed."""
    hits = []
    for hit in data:
        hits.append({
            "_id": str(hit.get("id")),
            '_source': hit,
        })
    data = {
        'total': len(data),
        'hits': {
            'hits': data,
            'max_score': None,
            'total': len(data),
        },
        'total': len(data),
        'took': 7,
        'start': 0,
        'perPage': len(data),
           "aggregations":{
              "agg_terms_price":{
                 "doc_count_error_upper_bound":0,
                 "sum_other_doc_count":1,
                 "buckets":[
                    {
                       "key":42,
                       "doc_count":1
                    },
                    {
                       "key":45,
                       "doc_count":1
                    },
                    {
                       "key":47,
                       "doc_count":1
                    },
                    {
                       "key":49,
                       "doc_count":1
                    },
                    {
                       "key":51,
                       "doc_count":1
                    },
                    {
                       "key":56.9900016784668,
                       "doc_count":1
                    },
                    {
                       "key":60,
                       "doc_count":1
                    },
                    {
                       "key":65,
                       "doc_count":1
                    },
                    {
                       "key":66,
                       "doc_count":1
                    },
                    {
                       "key":72,
                       "doc_count":1
                    }
                 ]
              },
              "agg_terms_erin_recommends":{
                 "doc_count_error_upper_bound":0,
                 "sum_other_doc_count":0,
                 "buckets":[
                    {
                       "key":0,
                       "doc_count":9
                    },
                    {
                       "key":1,
                       "doc_count":2
                    }
                 ]
              },
              "agg_terms_color_options":{
                 "doc_count_error_upper_bound":0,
                 "sum_other_doc_count":0,
                 "buckets":[
                    {
                       "key":49,
                       "doc_count":6
                    },
                    {
                       "key":58,
                       "doc_count":6
                    },
                    {
                       "key":50,
                       "doc_count":5
                    },
                    {
                       "key":53,
                       "doc_count":5
                    },
                    {
                       "key":56,
                       "doc_count":4
                    },
                    {
                       "key":60,
                       "doc_count":3
                    },
                    {
                       "key":57,
                       "doc_count":2
                    },
                    {
                       "key":52,
                       "doc_count":1
                    },
                    {
                       "key":59,
                       "doc_count":1
                    }
                 ]
              },
              "agg_range_price":{
                 "buckets":[
                    {
                       "key":"0.0-50.0",
                       "from":0,
                       "to":50,
                       "doc_count":4
                    },
                    {
                       "key":"50.0-100.0",
                       "from":50,
                       "to":100,
                       "doc_count":7
                    },
                    {
                       "key":"100.0-150.0",
                       "from":100,
                       "to":150,
                       "doc_count":0
                    },
                    {
                       "key":"150.0-*",
                       "from":150,
                       "doc_count":0
                    }
                 ]
              },
              "agg_terms_size_options":{
                 "doc_count_error_upper_bound":0,
                 "sum_other_doc_count":0,
                 "buckets":[
                    {
                       "key":167,
                       "doc_count":11
                    },
                    {
                       "key":168,
                       "doc_count":11
                    },
                    {
                       "key":169,
                       "doc_count":11
                    },
                    {
                       "key":170,
                       "doc_count":11
                    },
                    {
                       "key":171,
                       "doc_count":11
                    }
                 ]
              },
              "agg_terms_color":{
                 "doc_count_error_upper_bound":0,
                 "sum_other_doc_count":0,
                 "buckets":[

                 ]
              },
              "agg_terms_erin_recommends_options":{
                 "doc_count_error_upper_bound":0,
                 "sum_other_doc_count":0,
                 "buckets":[

                 ]
              },
              "agg_terms_size":{
                 "doc_count_error_upper_bound":0,
                 "sum_other_doc_count":0,
                 "buckets":[

                 ]
              }
           }
    }
    return werkzeug.wrappers.Response(
        status=status,
        content_type='application/json; charset=utf-8',
        headers=[
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ('Access-Control-Allow-Methods', 'GET'),
            #('Access-Control-Allow-Origin', 'http://localhost:3000'),
            #('Cache-Control: no-cache', 'private'),
            #('Connection', 'keep-alive'),
            #('Content-Encoding', 'gzip'),
            #('Content-Type: text/html', 'charset=UTF-8'),
            #('Date', 'Wed, 13 Mar 2019 18:18:47 GMT'),
            #('Server', 'nginx/1.13.6'),
            #('Transfer-Encoding', 'chunked'),
    ],
        response=json.dumps(data),
    )

def simple_response(data, status=200):
    return werkzeug.wrappers.Response(
        status=status,
        content_type='application/json; charset=utf-8',
        headers=[
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ('Access-Control-Allow-Methods', 'GET'),
            #('Access-Control-Allow-Origin', 'http://localhost:3000'),
            #('Cache-Control: no-cache', 'private'),
            #('Connection', 'keep-alive'),
            #('Content-Encoding', 'gzip'),
            #('Content-Type: text/html', 'charset=UTF-8'),
            #('Date', 'Wed, 13 Mar 2019 18:18:47 GMT'),
            #('Server', 'nginx/1.13.6'),
            #('Transfer-Encoding', 'chunked'),
    ],
        response=json.dumps(data),
    )

def invalid_response(typ, message=None, status=400):
    """Invalid Response
    This will be the return value whenever the server runs into an error
    either from the client or the server."""
    return werkzeug.wrappers.Response(
        status=status,
        content_type='application/json; charset=utf-8',
        response=json.dumps({
            'type': typ,
            'message': message if message else 'wrong arguments (missing validation)',
        }),
    )


def extract_arguments(payload, offset=0, limit=0, order=None):
    """."""
    fields, domain = [], []
    if payload.get('domain'):
        domain += ast.literal_eval(payload.get('domain'))
    if payload.get('fields'):
        fields += ast.literal_eval(payload.get('fields'))
    if payload.get('offset'):
        offset = int(payload['offset'])
    if payload.get('limit'):
        limit = int(payload['limit'])
    if payload.get('order'):
        order = payload.get('order')
    return [domain, fields, offset, limit, order]
