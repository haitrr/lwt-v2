import json
import os
from google.cloud import firestore
from urllib import parse
from flask import jsonify, Response

ALLOW_ORIGIN = 'Access-Control-Allow-Origin'


def cross_origin(allowed_methods="*", allowed_origins="*", allowed_headers="*"):
    def get_header_attr_value(value):
        if type(value) is str:
            return value
        if type(value) is list:
            return ",".join(value)
        raise Exception("value type not supported")

    def decorator(handler):
        def wrapped(request):
            def get_allowed_origins_value():
                if allowed_origins == "*":
                    return allowed_origins
                if "origin" not in request.headers:
                    return ""
                origin = request.headers['origin']
                if origin:
                    url = parse.urlparse(origin)
                    url = url._replace(netloc=url.hostname)
                    if url.geturl() in allowed_origins:
                        return origin
                return ""

            allowed_origin = get_allowed_origins_value()
            if request.method == 'OPTIONS':
                headers = {
                    ALLOW_ORIGIN: allowed_origin,
                    'Access-Control-Allow-Methods': get_header_attr_value(allowed_methods),
                    'Access-Control-Allow-Headers': get_header_attr_value(allowed_headers),
                }
                return '', 204, headers
            response = handler(request)
            if type(response) is Response:
                response.headers[ALLOW_ORIGIN] = allowed_origin
                return response

            if type(response) is tuple:
                headers = response[2]
                headers[ALLOW_ORIGIN] = allowed_origin
                return response[0], response[1], headers

            headers = {ALLOW_ORIGIN: allowed_origin}
            return response, 200, headers

        return wrapped

    return decorator


@cross_origin(allowed_methods=['GET'], allowed_origins=["http://localhost", "https://lwt-web.azurewebsites.net"])
def get_texts(request):
    json_creds = os.getenv("LWT_TEXTS_GCP_PROJECT_CREDENTIALS")
    json_creds = json_creds.replace(";", ",").replace("!", '=')
    json_creds = json.loads(json_creds)
    db = firestore.Client().from_service_account_info(json_creds)
    texts_ref = db.collection(u'texts')
    rs = []
    for doc in texts_ref.stream():
        rs.append(doc.to_dict())
    return jsonify(rs)
