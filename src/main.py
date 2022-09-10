import functions_framework
import google_photo
import twitter
import google.cloud.logging
import logging
import os

PROJECT_ID = os.environ.get('PROJECT_ID')
GOOGLE_OAUTH_CREDENITIALS_SECRET_ID = os.environ.get(
    'GOOGLE_OAUTH_CREDENITIALS_SECRET_ID')
TWITTER_CREDENITIALS_SECRET_ID = os.environ.get(
    'TWITTER_CREDENITIALS_SECRET_ID')
EXECUTE_ENV = os.environ.get('EXECUTE_ENV')

if EXECUTE_ENV == "LOCAL":
    logging.basicConfig(level=logging.DEBUG)
    for key, val in os.environ.items():
        logging.debug('{}: {}'.format(key, val))
else:
    # Cloud Loggingと統合。エラー発生箇所なども記録されるので便利。
    client = google.cloud.logging.Client()
    # デフォルトでINFO以上が収集される。
    client.setup_logging()


@functions_framework.cloud_event
def memory_tweet(cloud_event):
    # Google Photoから今日の写真をランダムで取得。
    google_oauth_credentials = google_photo.getCredentialsFromSecretManager(
        PROJECT_ID, GOOGLE_OAUTH_CREDENITIALS_SECRET_ID, 'latest')
    service = google_photo.getService(google_oauth_credentials)
    mediaItems = google_photo.getMediaItems(service)
    if len(mediaItems) == 0:
        logging.info("本日の写真はありません。")
        return

    mediaItem = google_photo.getRandomMediaItemsWithImageBinary(mediaItems)

    # Twitterに画像付きでツイート。
    twitter_credentials = twitter.getCredentialsFromSecretManager(
        PROJECT_ID, TWITTER_CREDENITIALS_SECRET_ID, 'latest')
    twitter.uploadMedia(mediaItem, twitter_credentials)
