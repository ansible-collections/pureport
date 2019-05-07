## Description
This is a collection of Ansible [library modules](https://docs.ansible.com/ansible/2.8/user_guide/modules_intro.html) which can
interact with the [Pureport](https://www.pureport.com/) ReST API.

It provides the following modules you can use in your own roles:
- `pureport_access_token_fact` - Obtain an OAuth access token which can be used as the `api_access_token` param 
  for all other modules in lieu of passing them the `api_key`/`api_secret`.  This allows other modules to skip their own retrieval 
  of the `access_token`, further reducing the number of API calls and execution time. 
- `pureport_location_facts` - used to list a set of locations
- `pureport_option_facts` - used to list a set of enum options used for creating connections
- `pureport_cloud_region_facts` - used to list a set of cloud region objects for various connection types
- `pureport_cloud_service_facts` - used to list a set of cloud service objects for public connections
- `pureport_account_facts` - used to list available accounts for an API key
- `pureport_supported_connection_facts` - used to list available supported connections for an account
- `pureport_network_facts` - used to list a set of networks
- `pureport_network` - used to create/update/delete a network
- `pureport_connection_facts` - used to list a set of connections
- `pureport_aws_direct_connect_connection` - used to create/update/delete a Pureport AWS connection
- `pureport_azure_express_route_connection` - used to create/update/delete a Pureport Azure Express Route connection
- `pureport_google_cloud_interconnect_connection` - used to create/update/delete a Pureport Google Cloud Interconnect connection
- `pureport_site_ipsec_vpn_connection` - used to create/update/delete a Pureport Site IPSec VPN connection

## Installation
This "role" is distributed via [ansible-galaxy](https://galaxy.ansible.com/) (bundled with Ansible).

```bash
ansible-galaxy install pureport.pureport-ansible-modules
```

Because this is not a collection of "roles" and is instead intended to be used within your own roles, you'll need to tell
Ansible where to find these modules and their utilities.

This can be done via Environment variables ([1](https://docs.ansible.com/ansible/2.8/dev_guide/developing_locally.html#adding-a-module-locally),
[1.1](https://docs.ansible.com/ansible/2.8/reference_appendices/config.html#envvar-ANSIBLE_LIBRARY),
[2](https://docs.ansible.com/ansible/2.8/reference_appendices/config.html?highlight=module_utils#envvar-ANSIBLE_MODULE_UTILS)):

```bash
ANSIBLE_GALAXY_ROLES_DIRECTORY="YOUR ANSIBLE GALAXY ROLES DIRECTORY"
PUREPORT_ANSIBLE_MODULES_DIR=${ANSIBLE_GALAXY_ROLES_DIRECTORY}/pureport.pureport-ansible-modules/ansible
export ANSIBLE_LIBRARY=${PUREPORT_ANSIBLE_MODULES_DIR}/modules
export ANSIBLE_MODULE_UTILS=${PUREPORT_ANSIBLE_MODULES_DIR}/module_utils
```

It can also be done via `ansible.cfg` file ([1](https://docs.ansible.com/ansible/2.8/reference_appendices/config.html#default-module-path),
[2](https://docs.ansible.com/ansible/2.8/reference_appendices/config.html#default-module-utils-path)):
```ini
[defaults]
library = ./roles/pureport.pureport-ansible-modules/ansible/modules
module_utils = ./roles/pureport.pureport-ansible-modules/ansible/module_utils
```

**NOTE:** The above assumes your Ansible Galaxy roles are installed to the `./roles` directory.

## Module Documentation
**NOTE**: This will only work with Ansible 2.8 (via this [PR](https://github.com/ansible/ansible/pull/50172)) which opens up
the `ANSIBLE_DOC_FRAGMENT_PLUGINS` environment variable for shared documentation in modules.

Because the modules for this are external to Ansible and some of the documentation is shared via 
[doc_fragments](https://docs.ansible.com/ansible/2.8/dev_guide/developing_modules_documenting.html#documentation-fragments), for 
documentation to work with the `ansible-doc`, simply do the following:
```bash
ANSIBLE_GALAXY_ROLES_DIRECTORY="YOUR ANSIBLE GALAXY ROLES DIRECTORY"
PUREPORT_ANSIBLE_MODULES_DIR=${ANSIBLE_GALAXY_ROLES_DIRECTORY}/pureport.pureport-ansible-modules/ansible
export ANSIBLE_DOC_FRAGMENT_PLUGINS=${PUREPORT_ANSIBLE_MODULES_DIR}/plugins/doc_fragments
```

It can also be done via `ansible.cfg` file ([1](https://docs.ansible.com/ansible/2.8/reference_appendices/config.html#doc-fragment-plugin-path))
```yaml
[defaults]
doc_fragment_plugins = ./roles/pureport.pureport-ansible-modules/ansible/plugins/doc_fragments
```

**NOTE:** The above assumes your Ansible Galaxy roles are installed to the `./roles` directory.

You can then get information about each module:
```bash
ansible-doc pureport_access_token_fact
ansible-doc pureport_location_facts
ansible-doc pureport_option_facts
ansible-doc pureport_cloud_region_facts
ansible-doc pureport_cloud_service_facts
ansible-doc pureport_account_facts
ansible-doc pureport_supported_connection_facts
ansible-doc pureport_network_facts
ansible-doc pureport_network
ansible-doc pureport_connection_facts
ansible-doc pureport_aws_direct_connect_connection
ansible-doc pureport_azure_express_route_connection
ansible-doc pureport_google_cloud_interconnect_connection
ansible-doc pureport_site_ipsec_vpn_connection
```

Also dump a snippet of what invoking a module requires:
```bash
ansible-doc pureport_access_token_fact -s
ansible-doc pureport_location_facts -s
ansible-doc pureport_option_facts -s
ansible-doc pureport_cloud_region_facts -s
ansible-doc pureport_cloud_service_facts -s
ansible-doc pureport_account_facts -s
ansible-doc pureport_supported_connection_facts -s
ansible-doc pureport_network_facts -s
ansible-doc pureport_network -s
ansible-doc pureport_connection_facts -s
ansible-doc pureport_aws_direct_connect_connection -s
ansible-doc pureport_azure_express_route_connection -s
ansible-doc pureport_google_cloud_interconnect_connection -s
ansible-doc pureport_site_ipsec_vpn_connection -s
```

## Examples
There are various examples on how to use these modules in the [examples directory](examples/README.md).