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
"""Flask-GAuth"""
import urllib.request
from urllib.parse import urljoin
import requests

from flask import render_template_string
from flask import request
from flask import session
from flask import url_for
from oauthlib.oauth2 import WebApplicationClient
from requests.auth import HTTPBasicAuth


class FlaskGoogleAuth(object):
    """A Flask extension to support authentication with Google."""

    def __init__(self, app=None):
        self._app = None
        self._client = None
        self._callback_endpoint = 'google_callback'
        if app:
            self.init_app(app)

    def init_app(self, app):
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

    @property
    def _redirect_url(self):
        redirect_url = urljoin(
            request.url_root, url_for(self._callback_endpoint))
        return redirect_url

    def _callback(self):
        token_url, _, body = self._client.prepare_token_request(
            token_url=self._app.config['GOOGLE_TOKEN_ENDPOINT'],
            authorization_response=request.url,
            redirect_url=self._redirect_url)
        auth = HTTPBasicAuth(
            self._app.config['GOOGLE_CLIENT_ID'],
            self._app.config['GOOGLE_CLIENT_SECRET'])
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        resp = requests.post(token_url, headers=headers, auth=auth, data=body)
        print(resp.json())
