# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "memory_tweet_source" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "/tmp/function.zip"
  excludes = [
    "venv",
    "__pycache__",
    ".gitignore",
  ]
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "memory_tweet_zip" {
  source       = data.archive_file.memory_tweet_source.output_path
  content_type = "application/zip"

  # Append to the MD5 checksum of the files's content
  # to force the zip to be updated as soon as a change occurs
  name   = "src-${data.archive_file.memory_tweet_source.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
}

# Create the Cloud function triggered by a `Finalize` event on the bucket
resource "google_cloudfunctions_function" "memory_tweet" {
  name    = "memory_tweet"
  runtime = "python39"

  # Get the source code of the cloud function as a Zip compression
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.memory_tweet_zip.name

  # Must match the function name in the cloud function `main.py` source code
  entry_point = "memory_tweet"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.memory_tweet_trigger.id
  }

  service_account_email = google_service_account.memory_tweet_function.email

}
