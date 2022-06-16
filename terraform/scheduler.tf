resource "google_cloud_scheduler_job" "memory_tweet" {
  name = "memory-tweet"
  # 1時間ごとに実行
  schedule  = "0 */1 * * *"
  time_zone = "Asia/Tokyo"

  pubsub_target {
    # NOTE: データは利用しないため、値は任意。
    data       = base64encode("memory tweet !!")
    topic_name = google_pubsub_topic.memory_tweet_trigger.id
  }

  retry_config {
    retry_count          = 1
    max_backoff_duration = "3600s"
    max_doublings        = 5
    max_retry_duration   = "0s"
    min_backoff_duration = "5s"
  }

}
