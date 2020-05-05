#!/usr/bin/env bash

account_id=$(pureport accounts create '{"name": "Ansible Testing"}' | jq  -r '.id')
pureport accounts consent -a "$account_id" accept > /dev/null
network_id=$(pureport accounts networks -a "$account_id" create '{"name": "Ansible Testing"}' | jq  -r '.id')
role_id=$(pureport accounts roles -a "$account_id" list | jq -r '.[0].id')
api_key=$(pureport accounts api-keys -a "$account_id" create '{"name": "Ansible Testing", "roles": [{"href": "'"$role_id"'"}]}')
api_key_key=$(echo "$api_key" | jq -r '.key')
api_key_secret=$(echo "$api_key" | jq -r '.secret')

echo "
Created account $account_id
Ansible Params:

---
api_key: $api_key_key
api_secret: $api_key_secret
account_href: /accounts/$account_id
network_href: /networks/$network_id
"
