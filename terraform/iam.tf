resource "google_secret_manager_secret_iam_member" "memory_tweet_function_google_oauth_credentials_secretaccessor" {
  secret_id = google_secret_manager_secret.google_oauth_credentials.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.memory_tweet_function.email}"
}
resource "google_secret_manager_secret_iam_member" "memory_tweet_function_google_oauth_credentials_secretversionadder" {
  secret_id = google_secret_manager_secret.google_oauth_credentials.id
  role      = "roles/secretmanager.secretVersionAdder"
  member    = "serviceAccount:${google_service_account.memory_tweet_function.email}"
}
resource "google_secret_manager_secret_iam_member" "memory_tweet_function_twitter_credentials_secretaccessor" {
  secret_id = google_secret_manager_secret.twitter_credentials.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.memory_tweet_function.email}"
}
resource "google_secret_manager_secret_iam_member" "memory_tweet_function_twitter_credentials_secretversionadder" {
  secret_id = google_secret_manager_secret.twitter_credentials.id
  role      = "roles/secretmanager.secretVersionAdder"
  member    = "serviceAccount:${google_service_account.memory_tweet_function.email}"
}
