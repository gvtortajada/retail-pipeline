provider "google-beta" {
  region  = var.region
}

provider "google" {
  region  = var.region
}

terraform {
  backend "gcs" {
    bucket = "<PROJECT_ID>-terraform-state"
  }
}

data "google_project" "project" {
    project_id = var.project_id
}

module "apis" {
  source      = "./apis"
  project_id = var.project_id
}

module "iam" {
  source      = "./iam"
  project_id  = var.project_id
  project_number = data.google_project.project.number
  depends_on  = [
    module.apis
  ]
}

module "secrets" {
  source      = "./secrets"
  project_id  = var.project_id
  api_user    = var.api_user
  api_secret  = var.api_secret
  depends_on  = [
    module.apis
  ]
}

module "network" {
  source                      = "./network"
  project_id                  = var.project_id
  region                      = var.region
  vpc-network                 = var.vpc-network
  sub_network                 = var.sub_network
  ip_cidr_range               = var.ip_cidr_range
  depends_on = [
    module.apis
  ]
}

module "composer" {
  source                      = "./composer"
  project_id                  = var.project_id
  region                      = var.region
  network                     = module.network.network
  subnetwork                  = module.network.subnetwork
  sa                          = module.iam.service_account
  api_auth_url                = var.api_auth_url
  api_products_url            = var.api_products_url
  api_categories_url          = var.api_categories_url
  retail_branch               = var.retail_branch
  composer_cron_scheduler     = var.composer_cron_scheduler
  composer_image_version      = var.composer_image_version
  depends_on = [
    module.apis,
    module.iam,
    module.network
  ]
}