variable "project_id" {}
variable "region" {}
variable "vpc-network" {}
variable "sub_network" {}
variable "ip_cidr_range" {}

resource "google_compute_network" "vpc_network" {
  project                 = var.project_id
  name                    = var.vpc-network
  auto_create_subnetworks = false
  mtu                     = 1460
}

resource "google_compute_subnetwork" "sub_network" {
    name                        = var.sub_network
    project                     = var.project_id
    ip_cidr_range               = var.ip_cidr_range
    region                      = var.region
    network                     = google_compute_network.vpc_network.id
    private_ip_google_access    = true
}

resource "google_compute_router" "router" {
  name    = "retail-router"
  project = var.project_id
  region  = google_compute_subnetwork.sub_network.region
  network = google_compute_network.vpc_network.id
}

resource "google_compute_address" "address" {
  name          = "nane-1-staticip"
  project       = var.project_id
  region        = var.region
  address_type  = "EXTERNAL"
}

resource "google_compute_router_nat" "nat_manual" {
  name      = "retail-router-nat"
  project   = var.project_id
  router    = google_compute_router.router.name
  region    = google_compute_router.router.region

  nat_ip_allocate_option = "MANUAL_ONLY"
  nat_ips                = google_compute_address.address.*.self_link

  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
  subnetwork {
    name                    = google_compute_subnetwork.sub_network.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
}

output "network" {
    value = google_compute_network.vpc_network
}

output "subnetwork" {
    value = google_compute_subnetwork.sub_network
}