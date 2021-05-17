#!/usr/bin/env python3

from werkzeug.exceptions import BadRequest, HTTPException, UnsupportedMediaType
from amazoncaptcha import AmazonCaptcha
from amazoncaptcha.exceptions import ContentTypeError
from flask import Flask, request, json
from PIL import UnidentifiedImageError
from requests.exceptions import RequestException
app = Flask(__name__)

HOST = "127.0.0.1"
PORT = 3003


@app.route("/resolve", methods=['POST', 'GET'])
def resolve():
    try:
        if request.method == 'POST':
            captcha = AmazonCaptcha(request.stream).solve()
        elif request.method == 'GET':
            captcha = AmazonCaptcha.fromlink(request.args.get('url')).solve()
        return {
            "meta": {
                "code": 200,
                "message": "Success"
            },
            "data": {
                "captcha": captcha
            }
        }
    except UnidentifiedImageError as e:
        raise UnsupportedMediaType("Provided image is invalid")
    except ContentTypeError as e:
        raise UnsupportedMediaType(e.__str__())
    except RequestException as e:
        raise BadRequest(e.__str__())


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "meta": {
            "code": e.code,
            "message": "{}: {}".format(e.name, getattr(e, 'description', ""))
        }
    })
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    from waitress import serve
    print("Starting HTTP server on", HOST, ":", PORT)
    serve(app, host=HOST, port=PORT)
