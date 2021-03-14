from flask import Flask, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user
import json
from oauthlib.oauth2 import WebApplicationClient
import os
import requests

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', None)
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise Exception('Unable to load Google app credentials')

GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth_client = WebApplicationClient(GOOGLE_CLIENT_ID)


class AuthenticatedUser:
    def __init__(self):
        self.is_authenticated = True  # TODO: True if the user has been logged in (gave a correct password)
        self.is_active = True  # TODO: True if the account is active and should be able to log in
        self.is_anonymous = False  # todo: not logged in user (i think?)

    def get_id(self):
        return u'user_identifier'  # todo: email or user id?


def _get_google_provider_config():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def init_auth_system(app: Flask):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        # TODO: find user based on identifier, or return none
        return {'username': 'bob', 'id': user_id}

    @app.route('/login')
    def login():
        google_provider_cfg = _get_google_provider_config()
        auth_endpoint = google_provider_cfg['authorization_endpoint']

        auth_request_url = oauth_client.prepare_request_uri(
            auth_endpoint,
            redirect_uri=url_for('login_callback', _external=True),
            scope=['openid', 'email']
        )
        return redirect(auth_request_url)

    @app.route('/login/callback')
    def login_callback():
        google_provider_config = _get_google_provider_config()

        user_code = request.args.get('code')
        token_endpoint = google_provider_config['token_endpoint']
        token_url, headers, body = oauth_client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=url_for('login_callback', _external=True),  # TODO: figure out how to handle login's next url
            code=user_code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
        )
        oauth_client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_request_url = google_provider_config['userinfo_endpoint']
        uri, headers, body = oauth_client.add_token(userinfo_request_url)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        email = userinfo_response.json()['email']

        # TODO: still need to set the logged in user and redirect to something

        return 'callback'

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
