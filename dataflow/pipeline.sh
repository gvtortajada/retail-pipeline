#!/bin/bash

PROJECT_ID=$1
echo $PROJECT_ID
gcloud config set project $PROJECT_ID
gcloud builds submit --tag gcr.io/$PROJECT_ID/retail-api-loader:latest
gsutil mb -p $PROJECT_ID -l northamerica-northeast1 -b on gs://$PROJECT_ID-retail-api-loader-dataflow-template
gsutil mb -p $PROJECT_ID -l northamerica-northeast1 -b on gs://$PROJECT_ID-retail-api-row-catalog-data
gsutil mb -p $PROJECT_ID -l northamerica-northeast1 -b on gs://$PROJECT_ID-temp-import-retail-api
gcloud dataflow flex-template build gs://$PROJECT_ID-retail-api-loader-dataflow-template/dataflow/templates/retail-api-loader.json \
  --image gcr.io/$PROJECT_ID/retail-api-loader:latest \
  --sdk-language "PYTHON" \
  --metadata-file "metadata.json"