# Google APIのOauthクレデンシャルを保存する。
# NOTE: 最初は人による認証が必要なため、初期のバージョンは手動作成する。
resource "google_secret_manager_secret" "google_oauth_credentials" {
  secret_id = "google-oauth-credentials"
  replication {
    automatic = true
  }
}