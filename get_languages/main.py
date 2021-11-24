from google.cloud import firestore
from urllib import parse
from flask import jsonify


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
                origin = request.headers['origin']
                if origin:
                    url = parse.urlparse(origin)
                    url = url._replace(netloc=url.hostname)
                    if url.geturl() in allowed_origins:
                        return origin
                return ""

            if request.method == 'OPTIONS':
                headers = {
                    'Access-Control-Allow-Origin': get_allowed_origins_value(),
                    'Access-Control-Allow-Methods': get_header_attr_value(allowed_methods),
                    'Access-Control-Allow-Headers': get_header_attr_value(allowed_headers),
                }
                return '', 204, headers
            return handler(request)

        return wrapped

    return decorator


@cross_origin(allowed_methods=['GET'], allowed_origins=["http://localhost", "https://haitran.dev"])
def get_languages(request):
    db = firestore.Client()
    languages_ref = db.collection(u'languages')
    rs = []
    for doc in languages_ref.stream():
        rs.append(doc.to_dict())
    return jsonify(rs)
