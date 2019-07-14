import ast
import json
import werkzeug.wrappers

host = "http://localhost:8069"
category_offset = 2
size_attribute_name = "Talla"
color_attribute_name = "Color"

def valid_response(data, status=200):
    """Valid response - This will be returned when the http request is successfully processed."""
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
        'took': 0,
        'start': 0,
        'perPage': len(data)
    }
    return werkzeug.wrappers.Response(
        status=status,
        content_type='application/json; charset=utf-8',
        headers=[
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'CONTENT-TYPE'),
            ('Access-Control-Allow-Methods', 'GET'),
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
    ],
        response=json.dumps(data),
    )

def invalid_response(typ, message=None, status=400):
    """Invalid response - This will be the returned value whenever the server runs into an error
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
