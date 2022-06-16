import google_photo
import twitter

PROJECT_ID = 'rising-beach-352202'
GOOGLE_OAUTH_CREDENITIALS_SECRET_ID = 'google-oauth-credentials'
TWITTER_CREDENITIALS_SECRET_ID = 'twitter-credentials'

google_oauth_credentials = google_photo.getCredentialsFromSecretManager(
    PROJECT_ID, GOOGLE_OAUTH_CREDENITIALS_SECRET_ID, 'latest')
service = google_photo.getService(google_oauth_credentials)
mediaItems = google_photo.getMediaItems(service)
mediaItem = google_photo.getRandomMediaItemsWithImageBinary(mediaItems)

twitter_credentials = twitter.getCredentialsFromSecretManager(
    PROJECT_ID, TWITTER_CREDENITIALS_SECRET_ID, 'latest')

twitter.uploadMedia(mediaItem, twitter_credentials)
