class memoryTweetError(Exception):
    """memoryTweetのベースException"""


class authError(memoryTweetError):
    """認証認可に関するエラー時に利用する"""


class googlePhoto(memoryTweetError):
    """googlePhotoに関するエラー時に利用する"""
