from google.cloud import firestore
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
            if request.method == 'OPTIONS':
                headers = {
                    'Access-Control-Allow-Origin': get_header_attr_value(allowed_origins),
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
