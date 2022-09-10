# Memory Tweet Bot on GCP Cloud Functions

今日の日付と同じ過去の画像をランダムにGoogle Photoから取得し、画像付きでツイートするBotです。例えば今日が2022/06/18の場合、Google PhotoからXXXX/06/18の写真をランダムで取得し、画像付きでツイートします。

# モチベーション

写真を撮る目的は様々です。私の場合は幸せな時間を思い出し、今を生きる力にすることが目的です。思い出は私に愛と勇気、そして圧倒的なパワーを与えます。しかし、ある日私は気づきました。「あれ、写真たくさん撮ってるけど見る頻度少なくない、、、？？」

データを溜めただけで満足してはいけません。どのように活用するかが重要なのです。そこで私は毎日チェックするTwitterで思い出を振り返れるようにしたのです。


# アーキテクチャ概要

![architecture](doc/images/architecture.svg)

Cloud Schedulerにより１時間ごとにCloud Functionsが実行され、Tweetをします。ランタイムはPythonです。Cloud Functionsは実行されると、Google Photoから写真を取得し、Twitterに画像付きでツイートをします。Google PhotoやTwitterで利用するクレデンシャルはSecret Managerに保存します。一部の初期構築以外は全てTerraformで管理できます。

# 構築手順
- [setup.md](./doc/setup.md)

# テスト

プロジェクトの設定とログイン

```
$ gcloud config set project memory-tweet-xxxx
$ gcloud auth application-default login
```

環境変数をセット

```
$ cd src

$ export PROJECT_ID=memory-tweet-xxxx
$ export EXECUTE_ENV='LOCAL'
$ export GOOGLE_OAUTH_CREDENITIALS_SECRET_ID='google-oauth-credentials'       
$ export TWITTER_CREDENITIALS_SECRET_ID='twitter-credentials'     

```

funcations-frameworkの実行
```
$ functions-framework --target=memory_tweet
```

違うタブでcurlする。

```
$ curl -X POST localhost:8080 \
   -H "Content-Type: application/cloudevents+json" \
   -d '{
"specversion" : "1.0",
"type" : "example.com.cloud.event",
"source" : "https://example.com/cloudevents/pull",
"subject" : "123",
"id" : "A234-1234-1234",
"time" : "2018-04-05T17:31:00Z",
"data" : "hello world"
}'
```
