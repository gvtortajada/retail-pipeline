#!/bin/bash

PROJECT_ID=$1
echo $PROJECT_ID
gcloud config set project $PROJECT_ID
gsutil mb -p $PROJECT_ID -l northamerica-northeast1 -b on gs://$PROJECT_ID-terraform-state
sed -i "s/<PROJECT_ID>/${PROJECT_ID}/g" main.tf
sed -i "s/<PROJECT_ID>/${PROJECT_ID}/g" variables.tf