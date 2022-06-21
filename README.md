# Memory Tweet Bot on GCP Cloud Functions

今日の日付と同じ過去の画像をランダムにGoogle Photoから取得し、画像付きでツイートするBotです。例えば今日が2022/06/18の場合、Google PhotoからXXXX/06/18の写真をランダムで取得し、画像付きでツイートします。

# モチベーション

写真を撮る目的は様々です。私の場合は幸せな時間を思い出し、今を生きる力にすることが目的です。思い出は私に愛と勇気、そして圧倒的なパワーを与えます。しかし、ある日私は気づきました。「あれ、写真たくさん撮ってるけど見る頻度少なくない、、、？？」

データを溜めただけで満足してはいけません。どのように活用するかが重要なのです。そこで私は毎日チェックするTwitterで思い出を振り返れるようにしたのです。


# アーキテクチャ

![architecture](doc/images/architecture.svg)

PythonをCloud Functions上で実行します。Cloud Schedulerにより１時間ごとににCloud Functionを実行しています。Google PhotoやTwitterで利用するクレデンシャルはSecret Managerに保存し、Cloud Functionから利用します。一部の初期構築以外は全てTerraformで管理できます。

# 構築
- [setup.md](./doc/setup.md)