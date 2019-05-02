# Test Playbooks

## Setup
Export the library/module_utils to your Ansible environment, so Ansible can find them.
```bash
PUREPORT_ANSIBLE_MODULES_DIR="THE PROJECT DIRECTORY HERE"
export ANSIBLE_LIBRARY=${PUREPORT_ANSIBLE_MODULES_DIR}/modules
export ANSIBLE_MODULE_UTILS=${PUREPORT_ANSIBLE_MODULES_DIR}/module_utils
export ANSIBLE_DOC_FRAGMENT_PLUGINS=${PUREPORT_ANSIBLE_MODULES_DIR}/plugins/doc_fragments
```

## Add a `group-vars/all.yml` using the following template:
```yaml
api_base_url: ""
api_key: ""
api_secret: ""

account_id: ""
account:
  id: ""
  href: /accounts/""

network_id: ""
network:
  id: ""
  href: /networks/""

```

## Run the tests
```bash
ansible-playbook main.yml
```

