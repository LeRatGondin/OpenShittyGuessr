import logging
from flask import Flask, request
import json
import requests
import re
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


config = json.load(open('config.json'))


@app.route('/connect')
def connect():
    code = request.args.get('code')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {config.get("client_secret")}',
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": config.get('client_id'),
    }
    response = requests.post(
        'https://graph.mapillary.com/token', headers=headers, data=data)
    response = response.json()
    print(response)
    config['access_token'] = response['access_token']
    json.dump(config, open('config.json', 'w'))
    return "You can now close this tab. And run the app."


if config.get('client_secret') == "" or config.get('client_id') == "":
    print("Please open the following link : https://www.mapillary.com/dashboard/developers, create an app and then paste the client secret")
    print("Don't forget to add http://localhost:8080/connect to the redirect url")
    client_secret = input("Enter the client secret: ")
    regex = r"MLY|"

    while client_secret is None or re.match(regex, client_secret) is None:
        client_secret = input("Enter the client secret: ")
    print("Please copy the client_id and then paste it right bellow")

    client_id = input("Enter the client id: ")
    while client_id.isnumeric() is False:
        client_id = input("Enter the client id: ")
    config['client_id'] = int(client_id)
    config['client_secret'] = client_secret
    json.dump(config, open('config.json', 'w'))
    print("Please run the setup again.")
    exit(0)
else:
    print(
        f"Please open the folowing link and authorise the app: https://www.mapillary.com/connect?client_id={config.get('client_id')}")
    print("\n"*5)
    app.run(port=8080, )
