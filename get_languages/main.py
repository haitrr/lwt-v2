from google.cloud import firestore
from flask_cors import cross_origin
from flask import json


@cross_origin(allowed_methods=['GET'], origins=["http://localhost", "https://haitran.dev"])
@json
def get_languages(request):
    db = firestore.Client()
    languages_ref = db.collection(u'languages')
    rs = []
    for doc in languages_ref.stream():
        rs.append(doc.to_dict())
    return json.dumps(rs)
