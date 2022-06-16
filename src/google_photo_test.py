import google_photo

PROJECT_ID = 'rising-beach-352202'
SECRET_ID = 'google-oauth-credentials'

credentials = google_photo.getCredentialsFromSecretManager(
    PROJECT_ID, SECRET_ID, 'latest')
service = google_photo.getService(credentials)
mediaItems = google_photo.getMediaItems(service)
mediaItem = google_photo.getRandomMediaItemsWithImageBinary(mediaItems)
with open('test.jpeg', 'wb') as f:
    f.write(mediaItem['imageBinary'])
