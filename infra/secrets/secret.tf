variable "project_id" {}
variable "api_user" {}
variable "api_secret" {}

resource "google_secret_manager_secret" "api-user" {
  secret_id = "api-user"
  project   = var.project_id

  labels = {
    label = "retail-api"
  }

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "api-secret" {
  secret_id = "api-secret"
  project   = var.project_id

  labels = {
    label = "retail-api"
  }

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "api-user-version" {
  secret      = google_secret_manager_secret.api-user.id
  secret_data = var.api_user
}

resource "google_secret_manager_secret_version" "api-secret-version" {
  secret      = google_secret_manager_secret.api-secret.id
  secret_data = var.api_secret
}