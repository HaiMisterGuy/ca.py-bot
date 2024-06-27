import asyncio
import json
import os
from flask import Flask, g, session, redirect, request, url_for, jsonify
from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse

API_ENDPOINT = "https://discordapp.com/api/v6"
API_AUTH_URL = API_ENDPOINT + "/oauth2/authorize"
API_TOKEN_URL = API_ENDPOINT + "/oauth2/token"
config_path = os.path.dirname(os.path.realpath(__file__)) + "/../config.json"
config = json.load(open(config_path))

parsed_redirect_uri = urlparse(config["redirect_uri"])
use_secure_callback = parsed_redirect_uri.scheme == "https"
port = parsed_redirect_uri.netloc.split(":")[1]
ssl_context = (config["crt_path"], config["key_path"]) if use_secure_callback else None

flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = config["client_secret"]

def token_updater(token):
    session["oauth2_token"] = token

def make_session(token = None, state = None, scope = None):
    return OAuth2Session(
        client_id = config["client_id"],
        token = token,
        state = state,
        scope = scope,
        redirect_uri = config["redirect_uri"],
        auto_refresh_kwargs = {
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
        },
        auto_refresh_url = API_TOKEN_URL,
        token_updater = token_updater
    )

@flask_app.route("/")
def index():
    scope = request.args.get(
        "scope",
        "identify email connections guilds guilds.join"
    )
    discord = make_session(scope = scope.split(" "))
    auth_url, state = discord.authorization_url(API_AUTH_URL)
    session["oauth2_state"] = state
    return redirect(auth_url)

@flask_app.route(parsed_redirect_uri.path)
def callback():
    if request.values.get("error"):
        return request.values["error"]
    discord = make_session(state = session.get("oauth2_state"))
    token = discord.fetch_token(
        API_TOKEN_URL,
        client_secret = config["client_secret"],
        authorization_response = request.url
    )
    print(token)
    session["oauth2_token"] = token
    return redirect(url_for(".me"))

@flask_app.route("/me")
def me():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_ENDPOINT + '/users/@me').json()
    guilds = discord.get(API_ENDPOINT + '/users/@me/guilds').json()
    connections = discord.get(API_ENDPOINT + '/users/@me/connections').json()
    return jsonify(user=user, guilds=guilds, connections=connections)

flask_app.run("0.0.0.0", port, debug = False, ssl_context = ssl_context)
