# Test Playbooks

## Setup
This *playbooks* directory already contains an `ansible.cfg` file that should setup the correct paths
for you, but if you wish to run these playbooks outside this directory, `export` the 
library/module_utils/doc_fragments to your Ansible environment.
```bash
PUREPORT_ANSIBLE_MODULES_DIR="THE PROJECT DIRECTORY HERE"
export ANSIBLE_LIBRARY=${PUREPORT_ANSIBLE_MODULES_DIR}/modules
export ANSIBLE_MODULE_UTILS=${PUREPORT_ANSIBLE_MODULES_DIR}/module_utils
export ANSIBLE_DOC_FRAGMENT_PLUGINS=${PUREPORT_ANSIBLE_MODULES_DIR}/plugins/doc_fragments
```

### Add a `host-vars/localhost.yml` using the following template:
```yaml
api_base_url: ""
api_key: ""
api_secret: ""

account_href: /accounts/""

network_href: /networks/""

location_href: /locations/""

cloud_service_hrefs:
  - /cloudServices/""
```

### Add a `group-vars/all.yml` using the following template:
```yaml
aws_account_id: ""

azure_service_key: ""

gci_primary_pairing_key: ""
gci_secondary_pairing_key: ""
```

## Run the tests
```bash
ansible-playbook main.yml
```

