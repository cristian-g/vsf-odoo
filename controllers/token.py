import logging
import json
import werkzeug.wrappers
from odoo import http
from odoo.http import request
from odoo.addons.restful.common import invalid_response, valid_response

_logger = logging.getLogger(__name__)

expires_in = 'restful.access_token_expires_in'


class APIToken(http.Controller):
    """."""

    def __init__(self):

        self._token = request.env['api.access_token']
        self._expires_in = request.env.ref(expires_in).sudo().value

    @http.route('/api/auth/token', methods=['GET'], type='http', auth='none', csrf=False)
    def token(self, **post):
        _token = request.env['api.access_token']
        params = ['db', 'login', 'password']
        params = {key: post.get(key) for key in params if post.get(key)}
        db, username, password = post.get(
            'db'), post.get('login'), post.get('password')
        if not all([db, username, password]):
            # Empty 'db' or 'username' or 'password:
            return invalid_response(400, 'missing error', 'either of the following are missing [db, username,password]')
        # Login in odoo database:
        try:
            request.session.authenticate(db, username, password)
        except Exception as e:
            # Invalid database:
            info = "The database name is not valid {}".format((e))
            error = 'invalid_database'
            _logger.error(info)
            return invalid_response(400, error, info)

        uid = request.session.uid
        # odoo login failed:
        if not uid:
            info = "authentication failed"
            error = 'authentication failed'
            _logger.error(info)
            return invalid_response(401, error, info)

        # Generate tokens
        access_token = _token.find_one_or_create_token(
            user_id=uid, create=True)
        # Successful response:
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=[('Cache-Control', 'no-store'),
                     ('Pragma', 'no-cache')],
            response=json.dumps({
                'uid': uid,
                'user_context': request.session.get_context() if uid else {},
                'company_id': request.env.user.company_id.id if uid else None,
                'access_token': access_token,
                'expires_in': self._expires_in,
            }),
        )

    @http.route('/api/auth/token', methods=['DELETE'], type='http', auth='none', csrf=False)
    def delete(self, **post):
        """."""
        _token = request.env['api.access_token']
        access_token = request.httprequest.headers.get('access_token')
        access_token = _token.search([('token', '=', access_token)])
        if not access_token:
            info = "No access token was provided in request!"
            error = 'no_access_token'
            _logger.error(info)
            return invalid_response(400, error, info)
        for token in access_token:
            token.unlink()
        # Successful response:
        return valid_response(
            200,
            {"desc": 'token successfully deleted', "delete": True}
        )
