#!/bin/bash
PROJECT_ID=$1
echo $PROJECT_ID
gcloud config set project $PROJECT_ID
terraform import \
    -var project_id=$PROJECT_ID \
    -var ip_cidr_range="10.128.0.0/24" \
    -var region="northamerica-northeast1" \
    -var vpc-network="retail-api-vpc" \
    -var sub_network="retail-api-subnet" \
    module.network.google_compute_address.address "nane-1-staticip"