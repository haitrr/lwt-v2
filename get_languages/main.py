from google.cloud import firestore

def get_languages(request):
    db = firestore.Client()
    texts_ref = db.collection(u'languages')
    rs = []
    for doc in texts_ref.stream():
        rs.append(doc)
    return rs
