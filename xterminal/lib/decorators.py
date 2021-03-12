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
"""Implements decorators for the xTerminal application."""
from functools import wraps

from flask import abort
from flask import current_app
from flask import redirect
from flask import session
from flask import url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login_view.login'))

        email = session['email']
        if email not in current_app.config['ALLOWED_EMAILS']:
            return abort(403)

        return func(*args, **kwargs)

    return wrapper
