from secret_manager import accessSecretVersion
import tweepy
import tempfile
import datetime
import json

URL_MEDIA = "https://upload.twitter.com/1.1/media/upload.json"
URL_TEXT = "https://api.twitter.com/1.1/statuses/update.json"


def getCredentialsFromSecretManager(project_id, secret_id, version_id):
    """
    API接続時に必要なクレデンシャルを取得する。
    """

    # NOTE: 初期構築時に手動でバージョンを追加する必要がある。
    credentials_raw = accessSecretVersion(project_id, secret_id, version_id)

    credentials = json.loads(credentials_raw)
    return credentials


def uploadMedia(mediaItem, credentials):
    """
    写真付きで日付をツイートをする。
    """

    # APIの認証
    auth = tweepy.OAuthHandler(
        credentials['TWITTER_CK'], credentials['TWITTER_CS'])
    auth.set_access_token(credentials['TWITTER_AT'], credentials['TWITTER_AS'])

    api = tweepy.API(auth)

    # JSTに変換する。
    t_delta = datetime.timedelta(hours=9)  # 9時間
    dt_utc = datetime.datetime.strptime(
        mediaItem['mediaMetadata']['creationTime'], '%Y-%m-%dT%H:%M:%SZ')
    dt_jst = dt_utc + t_delta
    message = dt_jst.strftime('%Y-%m-%d %H:%M:%S %Z')

    with tempfile.NamedTemporaryFile() as f:
        f.write(mediaItem['imageBinary'])
        api.update_status_with_media(filename=f.name, status=message)
