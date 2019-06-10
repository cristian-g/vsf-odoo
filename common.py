import ast
import json
import werkzeug.wrappers

def valid_response(data, status=200):
    """Valid Response
    This will be return when the http request was successfully processed."""
    data = {
        'hits': {
            'hits': data,
        },
        'total': len(data),
        'start': 0,
        'perPage': len(data),
        'aggregations': [],
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
