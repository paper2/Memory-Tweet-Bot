from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import google.oauth2.credentials
from secret_manager import addSecretVersion, accessSecretVersion, destroy_secret_version
import json
import datetime
import logging
import random
import requests
import exceptions

MAX_NUM_RETRY = 3
API_SERVICE_NAME = 'photoslibrary'
API_VERSION = 'v1'


def getCredentialsFromSecretManager(project_id, secret_id, version_id):
    """
    API接続時に必要なクレデンシャルを取得する。
    """

    # 認証情報をSecretManagerから取得。
    # NOTE: 初期構築時は手動でバージョンを追加する必要がある。
    credentials_raw = accessSecretVersion(project_id, secret_id, version_id)

    credentials_json = json.loads(credentials_raw)

    # クレデンシャルの作成
    credentials = google.oauth2.credentials.Credentials(
        credentials_json['token'],
        refresh_token=credentials_json['refresh_token'],
        token_uri=credentials_json['token_uri'],
        client_id=credentials_json['client_id'],
        client_secret=credentials_json['client_secret'],
        expiry=datetime.datetime.strptime(
            credentials_json['expiry'], '%Y-%m-%dT%H:%M:%S.%fZ')
    )

    if not credentials or not credentials.valid:
        # 有効期限が切れていた場合更新
        if credentials and credentials.expired and credentials.refresh_token:
            logging.info('Credential refresh.')
            credentials.refresh(Request())
            # Secret Managerに更新したクレデンシャルを保存
            version_id = addSecretVersion(
                project_id, secret_id, credentials.to_json())
            # 古いVersionを削除。
            old_version_id = version_id - 1
            destroy_secret_version(project_id, secret_id, old_version_id)
        else:
            raise exceptions.authError('トークンが不正です。')

    return credentials


def getService(credentials):
    '''
    service objectの取得。
    '''

    service = build(API_SERVICE_NAME, API_VERSION,
                    credentials=credentials, static_discovery=False)
    return service


def getMediaItems(service):
    '''
    実行日と日付が同じMediaItemsを全て取得する。
    EX) 2019/09/22日に実行した場合は、xxxx/09/22に保存されたMediaItemsを取得する。

    NOTE: Google Photo APIの仕様上、JSTで利用する場合00:00(JST)~09:00(JST)の間は前日の写真が取得されてしまう。
    '''

    t_delta = datetime.timedelta(hours=9)  # 9時間
    JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差の「JST」タイムゾーン
    today = datetime.datetime.now(JST)
    body = {
        'pageSize': 100,
        'filters': {
            # "includedContentCategories"により、PEOPELなどカテゴリでフィルタできる。適宜活用する。
            # https://developers.google.com/photos/library/reference/rest/v1/mediaItems/search#contentcategory
            'contentFilter': {'includedContentCategories': ['NONE']},
            # NOTE: datesのフィルターはday（UTC）までしか指定できない。そのため00:00(JST)~09:00(JST)の間は前日の写真が取得されてしまう。
            #       上記制約の影響を緩和するためにJSTで日にちを指定しているが、返却される時刻はUTCなので注意。
            'dateFilter': {'dates': [{'year': 0, 'month': today.month, 'day': today.day}]},
            'mediaTypeFilter': {'mediaTypes': ['PHOTO']}
        }
    }
    mediaItems = []
    pagesize = 0
    response = {'nextPageToken': None}
    while 'nextPageToken' in response.keys():
        # 検索を実行。
        response = service.mediaItems().search(
            body=body).execute(num_retries=MAX_NUM_RETRY)

        if 'mediaItems' in response.keys():
            pagesize += len(response['mediaItems'])
            mediaItems += response['mediaItems']
        if 'nextPageToken' in response.keys():
            body['pageToken'] = response['nextPageToken']

        logging.debug('Get pagesize Sum: ' + str(pagesize))

    return mediaItems


def getRandomMediaItemsWithImageBinary(mediaItems):
    '''
    mediaItemsからランダムに1個を選択し、写真のバイナリを追加して返す。
    '''

    if len(mediaItems) == 0:
        logging.info("A number of MediaItems is 0.")
        return None

    # mediaItemsからランダムに要素を選択。
    mediaItem = random.choice(mediaItems)

    # 写真のバイナリを取得
    response = requests.get(mediaItem['baseUrl'])
    if response.status_code != 200:
        raise exceptions.googlePhoto("Getting an image was failed.")

    # 写真のバイナリを追加。
    mediaItem['imageBinary'] = response.content
    return mediaItem
