import functions_framework
import google_photo
import twitter

PROJECT_ID = 'rising-beach-352202'
GOOGLE_OAUTH_CREDENITIALS_SECRET_ID = 'google-oauth-credentials'
TWITTER_CREDENITIALS_SECRET_ID = 'twitter-credentials'


@functions_framework.cloud_event
def memory_tweet(cloud_event):
    # Google Photoから今日の写真をランダムで取得。
    google_oauth_credentials = google_photo.getCredentialsFromSecretManager(
        PROJECT_ID, GOOGLE_OAUTH_CREDENITIALS_SECRET_ID, 'latest')
    service = google_photo.getService(google_oauth_credentials)
    mediaItems = google_photo.getMediaItems(service)
    mediaItem = google_photo.getRandomMediaItemsWithImageBinary(mediaItems)

    # Twitterに画像付きでツイート。
    twitter_credentials = twitter.getCredentialsFromSecretManager(
        PROJECT_ID, TWITTER_CREDENITIALS_SECRET_ID, 'latest')
    twitter.uploadMedia(mediaItem, twitter_credentials)
