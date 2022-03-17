# the <PROJECT_ID> will be updated by the create_state_bucket.sh script
variable "project_id" {
  description = "the project id"
  default = "<PROJECT_ID>"  
}

variable "region" {
  description = "The region"
  default     = "northamerica-northeast1"
}

variable "zones" {
  type        = list(string)
  description = "The zone"
  default     = ["northamerica-northeast1-a"]
}

variable "ip_cidr_range" {
  default = "10.128.0.0/24"
}

variable "vpc-network" {
  description = "The VPC network"
  default     = "retail-api-vpc"
}

variable "sub_network" {
  description = "The subnetwork"
  default     = "retail-api-subnet"
}

variable "api_user" {
  default = "test1"  
}

variable "api_secret" {
  default = "test2"
}

variable "retail_branch" {
  default = "0"
}

variable "api_auth_url" {
  default = ""
}

variable "api_products_url" {
  default = ""
}

variable "api_categories_url" {
  default = ""
}

variable "composer_cron_scheduler" {
  default = "0 0 * * *"
}

variable "composer_image_version" {
  default = "composer-2.0.6-airflow-2.2.3"
}