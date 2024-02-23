from flask import Flask, request
import json
import requests
app = Flask(__name__)

print("Please open the folowing link and authorise the app: https://www.mapillary.com/connect?client_id=7240765502682683")


@app.route('/connect')
def connect():
    code = request.args.get('code')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth MLY|7240765502682683|1def76868ca59190281fb02e29592639',
    }

    data = """
    {
        "grant_type": "authorization_code",
        "code": " """ + code + """ ",
        "client_id": 7240765502682683, 
    }"""

    response = requests.post(
        'https://graph.mapillary.com/token', headers=headers, data=data)
    response = response.json()
    json.dump({"access_token": response["access_token"]}, open(
        'config.json', 'w'))
    return "You can now close this tab. And run the app."


app.run(port=8080)
