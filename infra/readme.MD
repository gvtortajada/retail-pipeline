# Provision infrastructure

## If already having a private IP

Replace <project_id> placeholder by your project id
```
./create_state_bucket.sh <project_id>
terraform init
./import_external_ip.sh <project_id>
terraform plan
```

Replace <...> placeholdera by Hybris api_user, api_secret, api_auth_url, api_products_url and api_categories_url
```
terraform apply -auto-approve \
    -var api_user=<api_user> \
    -var api_secret=<api_secret> \
    -var api_auth_url=<api_auth_url> \
    -var api_products_url=<api_products_url> \
    -var api_categories_url=<api_categories_url>
```

## If not having a private IP

Replace <project_id> placeholder by your project id
```
./create_state_bucket.sh <project_id>
terraform init
terraform plan
```

Replace <...> placeholdera by Hybris api_user, api_secret, api_auth_url, api_products_url and api_categories_url
```
terraform apply -auto-approve \
    -var api_user=<api_user> \
    -var api_secret=<api_secret> \
    -var api_auth_url=<api_auth_url> \
    -var api_products_url=<api_products_url> \
    -var api_categories_url=<api_categories_url>
```