import json

from google.cloud import firestore

def get_languages(request):
    db = firestore.Client()
    languages_ref = db.collection(u'languages')
    rs = []
    for doc in languages_ref.stream():
        rs.append(doc.to_dict())
    return json.dumps(rs)
