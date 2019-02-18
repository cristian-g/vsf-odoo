import functools
import logging
import json
import werkzeug.wrappers
from odoo import http
from odoo.http import request
from odoo.addons.restful.common import valid_response, invalid_response, extract_arguments

_logger = logging.getLogger(__name__)


def validate_token(func):
    """."""
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        """."""
        access_token = request.httprequest.headers.get('access_token')
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
    @http.route('/api/profile', type='http', auth="none", methods=['GET'], csrf=False)
    def get(self, model=None, id=None, **payload):

        data = request.env['res.users'].sudo().search_read(domain=[('id', '=', request.session.uid)], fields=['id', 'login'], offset=None, limit=1, order=None)
        if data:
            return valid_response(data)
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
