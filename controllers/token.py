import logging
import json
import werkzeug.wrappers
from odoo import http
from odoo.http import request, Response
from odoo.addons.vue_storefront.common import invalid_response, valid_response, simple_response

_logger = logging.getLogger(__name__)

expires_in = 'vue_storefront.access_token_expires_in'

class TokenAPIController(http.Controller):
    """."""

    def __init__(self):

        self._token = request.env['api.access_token']
        self._expires_in = request.env.ref(expires_in).sudo().value

    @http.route('/api/user/login', methods=['OPTIONS'], type='http', auth='none', csrf=False)
    def log_in_options(self, **post):

        data = {
            'items': 0,
            'start': 0,
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

    @http.route('/api/user/login', methods=['POST'], type='http', auth='none', csrf=False)
    def log_in(self, **post):

        body = request.httprequest.get_data()
        body_json = json.loads(body.decode("utf-8"))

        _token = request.env['api.access_token']
        db = 'odoo'

        username = body_json.get('username')
        password = body_json.get('password')

        if not all([db, username, password]):
            # Empty 'db' or 'username' or 'password:
            error_info = {
                "code": 500,
                "result": "You did not sign in correctly or your account is temporarily disabled."
            }
            return simple_response(error_info, 400)
        # Login in odoo database:
        try:
            request.session.authenticate(db, username, password)
        except Exception as e:
            # Invalid database:
            info = "The database name is not valid {}".format((e))
            error = 'invalid_database'
            _logger.error(info)
            error_info = {
                "code": 500,
                "result": "You did not sign in correctly or your account is temporarily disabled."
            }
            return simple_response(error_info, 400)

        uid = request.session.uid
        # odoo login failed:
        if not uid:
            info = "authentication failed"
            error = 'authentication failed'
            _logger.error(info)
            error_info = {
                "code": 500,
                "result": "You did not sign in correctly or your account is temporarily disabled."
            }
            return simple_response(error_info, 400)

        # Generate tokens
        access_token = _token.find_one_or_create_token(
            user_id=uid, create=True)
        # Successful response:
        return simple_response(
            {
                "code": 200,
                "result": access_token,
                "meta": {
                    "refreshToken": "refreshToken"
                }
            },
            200,
        )

    @http.route('/api/user/logout', methods=['OPTIONS'], type='http', auth='none', csrf=False)
    def log_out_options(self, **post):
        data = {}
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

    @http.route('/api/user/logout', methods=['DELETE'], type='http', auth='none', csrf=False)
    def log_out(self, **post):
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
