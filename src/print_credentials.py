import google_auth_oauthlib

CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRET_FILE, scopes=SCOPES)
credentials = flow.run_console()

print('CREDENTIALS_JSON: ' + credentials.to_json())
