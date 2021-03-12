# Copyright 2021 by TNiaH <kainguyen1509@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Flask-GoogleLogin"""
import urllib.request
from base64 import b64encode
from urllib.error import HTTPError
from urllib.parse import urljoin

from flask import abort
from flask import redirect
from flask import render_template_string
from flask import request as flask_req
from flask import session
from flask import url_for
from oauthlib.oauth2 import MismatchingStateError
from oauthlib.oauth2 import OAuth2Error
from oauthlib.oauth2 import WebApplicationClient


class FlaskGoogleLogin(object):
    """A Flask extension to support authentication with Google."""

    def __init__(self, app=None, redirected_endpoint=None, login_endpoint=None):
        self._app = None
        self._client = None
        self._callback_endpoint = 'google_callback'
        self.redirected_endpoint = redirected_endpoint
        self.login_endpoint = login_endpoint
        self.hooks = set()
        if app:
            self.init_app(app)

    def init_app(self, app, redirected_endpoint=None, login_endpoint=None):
        if not app.config.get('GOOGLE_CLIENT_ID'):
            raise RuntimeError(
                'Missing "GOOGLE_CLIENT_ID" in configuration.')

        if not app.config.get('GOOGLE_CLIENT_SECRET'):
            raise RuntimeError(
                'Missing "GOOGLE_CLIENT_SECRET" in configuration.')

        app.config.setdefault(
            'GOOGLE_AUTHORIZE_URI',
            'https://accounts.google.com/o/oauth2/auth')
        app.config.setdefault(
            'GOOGLE_TOKEN_ENDPOINT',
            'https://oauth2.googleapis.com/token')
        app.config.setdefault(
            'GOOGLE_SCOPES', ['email', 'profile', 'openid'])

        if redirected_endpoint is not None:
            self.redirected_endpoint = redirected_endpoint

        if login_endpoint is not None:
            self.login_endpoint = login_endpoint

        app.add_url_rule(
            '/login/google/callback',
            endpoint=self._callback_endpoint,
            view_func=self._callback)
        self._client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])
        self._app = app

    def google_login(self, g_class=None, g_icon=None):
        state = self._client.state_generator()
        session['state'] = state
        authorization_url = self._client.prepare_request_uri(
            uri=self._app.config['GOOGLE_AUTHORIZE_URI'],
            redirect_uri=self._redirect_url,
            scope=self._app.config['GOOGLE_SCOPES'],
            state=state,
            access_type='offline',
            prompt='select_account')
        return render_template_string(
            """
            <a href="{{ authorization_url }}"
            {% if g_class %}class="{{ g_class }}"{% endif %}>
            {% if g_icon %}
            <span class="{{ g_icon }} mr-3" aria-hidden="true"></span>
            {% endif %}
            Login with Google
            </a>
            """,
            authorization_url=authorization_url,
            g_class=g_class,
            g_icon=g_icon)

    def _callback(self):
        try:
            token_url, headers, body = self._client.prepare_token_request(
                token_url=self._app.config['GOOGLE_TOKEN_ENDPOINT'],
                authorization_response=flask_req.url,
                redirect_url=self._redirect_url,
                state=session.get('state', True))
        except MismatchingStateError:
            return redirect(url_for(self.login_endpoint))
        except OAuth2Error as e:
            self._app.logger.warning(
                'Error while preparing token request: %s' % e)
            return abort(500)

        headers.update({
            'Accept': 'application/json',
            'Authorization': self._basic_auth_string
        })
        req = urllib.request.Request(
            token_url,
            data=body.encode('utf-8'),
            headers=headers,
            method='POST')
        try:
            r = urllib.request.urlopen(req)
            data = self._client.parse_request_body_response(r.read())
        except HTTPError as e:
            err_msg = e.read().decode()
            self._app.logger.warning(
                'Error while fetching token: HTTP_STATUS_CODE_%s (%s)' % (
                    e.code, err_msg))
            return abort(500)

        for hook in self.hooks:
            hook(data)
        return redirect(url_for(self.redirected_endpoint))

    @property
    def _redirect_url(self):
        redirect_url = urljoin(
            flask_req.url_root, url_for(self._callback_endpoint))
        return redirect_url

    @property
    def _basic_auth_string(self):
        return 'Basic ' + b64encode(b':'.join((
            self._app.config['GOOGLE_CLIENT_ID'].encode('latin1'),
            self._app.config['GOOGLE_CLIENT_SECRET'].encode('latin1'))
        )).strip().decode('ascii')

    def register_hook(self, hook):
        """Registers a hook for token response."""
        self.hooks.add(hook)
