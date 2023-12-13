from firebase_admin import initialize_app, credentials

cred = credentials.Certificate('serviceAccountKey.json')
firebase = initialize_app(cred)

