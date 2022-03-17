variable "project_id" {}
variable "project_number" {}

resource "google_project_organization_policy" "requireOsLogin" {
  project     = var.project_id
  constraint = "compute.requireOsLogin"
 
  boolean_policy {
    enforced = false
  }
}

resource "google_project_organization_policy" "requireShieldedVm" {
  project     = var.project_id
  constraint = "compute.requireShieldedVm"
 
  boolean_policy {
    enforced = false
  }
}

resource "google_project_organization_policy" "restrictVpcPeering" {
    project     = var.project_id
    constraint = "compute.restrictVpcPeering"
 
    list_policy {
        allow {
            all = true
        }
    }
}

resource "google_service_account" "sa" {
    account_id   = "retail-api-sa"
    display_name = "Retail API SA"
    project      = var.project_id
}

resource "google_project_iam_member" "composer-worker" {
    project = var.project_id
    role    = "roles/composer.worker"
    member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "serviceAgent" {
    project = var.project_id
    role    = "roles/composer.serviceAgent"
    member  = "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "ServiceAgentV2Ext" {
    project = var.project_id
    role    = "roles/composer.ServiceAgentV2Ext"
    member  = "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "serviceAccountUser" {
    project = var.project_id
    role    = "roles/iam.serviceAccountUser"
    member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "dataflow-admin" {
    project = var.project_id
    role    = "roles/dataflow.admin"
    member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "dataflow-worker" {
    project = var.project_id
    role    = "roles/dataflow.worker"
    member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "storage-admin" {
    project = var.project_id
    role    = "roles/storage.admin"
    member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "bigquery-admin" {
    project = var.project_id
    role    = "roles/bigquery.admin"
    member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "dataflow-serviceAgent" {
    project = var.project_id
    role    = "roles/dataflow.serviceAgent"
    member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "secretmanager-secretAccessor" {
    project = var.project_id
    role    = "roles/secretmanager.secretAccessor"
    member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "retail-editor" {
    project = var.project_id
    role    = "roles/retail.editor"
    member  = "serviceAccount:${google_service_account.sa.email}"
}

output "service_account" {
    value = google_service_account.sa
}