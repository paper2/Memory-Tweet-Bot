# Cloud FunctionsのコードをZIPにします。
data "archive_file" "memory_tweet_source" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "/tmp/function.zip"
  excludes = [
    "venv",
    "__pycache__",
    ".gitignore",
    "client_secret.json",
  ]
}

# 作ったZIPをCloud Storageにuploadします。
resource "google_storage_bucket_object" "memory_tweet_zip" {
  source       = data.archive_file.memory_tweet_source.output_path
  content_type = "application/zip"

  # ファイル内容からMD5を作成し、ファイル名とします。
  # これでソースコードの変更時にCloud Funcationsが更新されるようになります。
  name   = "src-${data.archive_file.memory_tweet_source.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
}

# クラウドスケジューラーにより実行されるCloud Funcationを作成。
resource "google_cloudfunctions_function" "memory_tweet" {
  name    = "memory_tweet"
  runtime = "python39"

  available_memory_mb = 256

  # Cloud Functionのコードが入ったZIPを指定します。
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.memory_tweet_zip.name

  entry_point = "memory_tweet"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.memory_tweet_trigger.id
  }

  service_account_email = google_service_account.memory_tweet_function.email

  environment_variables = {
    PROJECT_ID                          = var.project_id
    GOOGLE_OAUTH_CREDENITIALS_SECRET_ID = google_secret_manager_secret.google_oauth_credentials.secret_id
    TWITTER_CREDENITIALS_SECRET_ID      = google_secret_manager_secret.twitter_credentials.secret_id
  }
}