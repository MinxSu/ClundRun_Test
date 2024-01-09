import os
import time
import requests
from requests import RequestException
from flask import Flask
from fastapi import Response, status

counter = 0
url = "https://api-server-blg4gtql7a-de.a.run.app/call_start"  # os.environ.get('SERVICE_URL')

print('server startup')

app = Flask(__name__)


@app.route("/call_start/")
def called():
    time.sleep(10)
    return "finish"


@app.route('/pubsub_receiver/', methods=['POST'])
def pubsub() -> Response:
    # call call_start
    try:
        call_test_service()
        time.sleep(10)
        return app.response_class(
            response="called",
            status=302,
            mimetype='application/json'
        )
    except Exception as e:
        print(e)
        return app.response_class(
            response=e,
            status=202,
            mimetype='application/json'
        )


def call_test_service():
    global counter
    # call call_start
    try:
        while counter < 15:
            counter += 1
            res = requests.get(url, timeout=30)
            print(f'current counter: {counter}')
            while res.content == b'finish':
                res = requests.get(url, timeout=30)
            counter -= 1
    except RequestException as e:
        print(e)


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=False)
