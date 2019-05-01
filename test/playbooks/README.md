# Test Playbooks

## Setup
Export the library/module_utils to your Ansible environment, so Ansible can find them.
```bash
export ANSIBLE_LIBRARY=$HOME/pureport-ansible-modules/library
export ANSIBLE_MODULE_UTILS=$HOME/pureport-ansible-modules/module_util
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

