variable "project_id" {}
variable "region" {}
variable "network" {}
variable "subnetwork" {}
variable "sa" {}
variable "api_auth_url" {}
variable "api_products_url" {}
variable "api_categories_url" {}
variable "retail_branch" {}
variable "composer_cron_scheduler" {}
variable "composer_image_version" {}

resource "google_composer_environment" "composer" {
  name      = "retail-api-composer"
  project   = var.project_id 
  region    = var.region
  config {

    software_config {
        image_version = var.composer_image_version
        pypi_packages = {
            google-cloud-retail = ""
        }
        airflow_config_overrides = {
            core-dags_are_paused_at_creation = "True"
        }
        env_variables = {
            PROJECT_ID      = var.project_id
            CONFIG_INI      = "gs://${var.project_id}-retail-api-row-catalog-data/config.INI"
            AUTH_URL        = var.api_auth_url
            PRODUCTS_URL    = var.api_products_url
            CATEGORIES_URL  = var.api_categories_url
            RETAIL_BRANCH   = var.retail_branch
            CRON_SCHEDULER  = var.composer_cron_scheduler
        }
    }

    workloads_config {
      scheduler {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
        count      = 1
      }
      web_server {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
      }
      worker {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
        min_count  = 1
        max_count  = 3
      }


    }
    environment_size = "ENVIRONMENT_SIZE_SMALL"

    node_config {
      network               = var.network.id
      subnetwork            = var.subnetwork.id
      service_account       = var.sa.name
    }

    private_environment_config {
        enable_private_endpoint = false
    }
  }
}

