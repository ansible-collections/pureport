## pureport.fabric
This is an [Ansible Collection](https://docs.ansible.com/ansible/latest/user_guide/collections_using.htmll) of various
[library modules](https://docs.ansible.com/ansible/latest/user_guide/modules_intro.html) which can interact with the
[Pureport](https://www.pureport.com/) ReST API.

## Installation
This collection is distributed via [ansible-galaxy](https://galaxy.ansible.com/pureport/fabric).

For compatibility between Ansible versions and the Python [pureport-client](https://pypi.org/project/pureport-client/) required dependency,
please use the following install methods matching your Ansible version:

| Pureport Collection Version                                                         | Ansible Version | [Pureport Client Version](https://pypi.org/project/pureport-client/) | Install Method                                                  |
| ----------------------------------------------------------------------------------- | --------------- | -------------------------------------------------------------------- | --------------------------------------------------------------- |
| [0.10.0+](https://galaxy.ansible.com/pureport/fabric)                               | 2.8+            | 1.0.0+                                                               | `ansible-galaxy collection install pureport.fabric`             |
| [0.0.9](https://galaxy.ansible.com/pureport/pureport)                               | 2.8+            | 0.0.8                                                                | `ansible-galaxy collection install pureport.pureport`           |
| [0.0.5 (Galaxy role)](https://galaxy.ansible.com/pureport/pureport_ansible_modules) | 2.7             | 0.0.8                                                                | `ansible-galaxy role install pureport.pureport_ansible_modules` |

### Modules
It provides the following modules you can use in your own roles:

| Name                                  | Description                                                                                           |
|---------------------------------------|-------------------------------------------------------------------------------------------------------|
|`access_token_info`                    | Obtain an OAuth access token which can be used as the `api_access_token` param for all other modules. |
|`locations_info`                       | List a set of locations                                                                               |
|`facilities_info`                      | List a set of facilities                                                                              |
|`options_info`                         | List a set of enum options used for creating connections                                              |
|`cloud_regions_info`                   | List a set of cloud region objects for various connection types                                       |
|`cloud_services_info`                  | List a set of cloud service objects for public connections                                            |
|`accounts_info`                        | List available accounts for an API key                                                                |
|`supported_connections_info`           | List available supported connections for an account                                                   |
|`supported_ports_info`                 | List available supported ports                                                                        |
|`ports_info`                           | List ports for an account                                                                             |
|`port`                                 | Create/update/delete a port                                                                           |
|`networks_info`                        | List a set of networks                                                                                |
|`network`                              | Create/update/delete a network                                                                        |
|`connections_info`                     | List a set of connections                                                                             |
|`aws_direct_connect_connection`        | Create/update/delete a Pureport AWS connection                                                        |
|`azure_express_route_connection`       | Create/update/delete a Pureport Azure Express Route connection                                        |
|`google_cloud_interconnect_connection` | Create/update/delete a Pureport Google Cloud Interconnect connection                                  |
|`port_connection`                      | Create/update/delete a Pureport Port connection                                                       |
|`site_ipsec_vpn_connection`            | Create/update/delete a Pureport Site IPSec VPN connection                                             |

## Module Documentation
You can then get information about each module:
```bash
ansible-doc pureport.fabric.access_token_info
ansible-doc pureport.fabric.locations_info
ansible-doc pureport.fabric.facilities_info
ansible-doc pureport.fabric.options_info
ansible-doc pureport.fabric.cloud_regions_info
ansible-doc pureport.fabric.cloud_services_info
ansible-doc pureport.fabric.accounts_info
ansible-doc pureport.fabric.supported_connections_info
ansible-doc pureport.fabric.supported_ports_info
ansible-doc pureport.fabric.ports_info
ansible-doc pureport.fabric.port
ansible-doc pureport.fabric.networks_info
ansible-doc pureport.fabric.network
ansible-doc pureport.fabric.connections_info
ansible-doc pureport.fabric.aws_direct_connect_connection
ansible-doc pureport.fabric.azure_express_route_connection
ansible-doc pureport.fabric.google_cloud_interconnect_connection
ansible-doc pureport.fabric.port_connection
ansible-doc pureport.fabric.site_ipsec_vpn_connection
```

Also dump a snippet of what invoking a module requires:
```bash
ansible-doc pureport.fabric.access_token_info -s
ansible-doc pureport.fabric.facilities_info -s
ansible-doc pureport.fabric.locations_info -s
ansible-doc pureport.fabric.options_info -s
ansible-doc pureport.fabric.cloud_regions_info -s
ansible-doc pureport.fabric.cloud_services_info -s
ansible-doc pureport.fabric.accounts_info -s
ansible-doc pureport.fabric.supported_connections_info -s
ansible-doc pureport.fabric.supported_ports_info -s
ansible-doc pureport.fabric.ports_info -s
ansible-doc pureport.fabric.port -s
ansible-doc pureport.fabric.networks_info -s
ansible-doc pureport.fabric.network -s
ansible-doc pureport.fabric.connections_info -s
ansible-doc pureport.fabric.aws_direct_connect_connection -s
ansible-doc pureport.fabric.azure_express_route_connection -s
ansible-doc pureport.fabric.google_cloud_interconnect_connection -s
ansible-doc pureport.fabric.port_connection -s
ansible-doc pureport.fabric.site_ipsec_vpn_connection -s
```

### Obtaining an `api_access_token`
Pureport's API heavily relies on an OAuth2 authentication schema.  For all the modules listed above, you can
pass `api_access_key` and `api_secret_key` to each of the modules for authentication.  Alternatively, the more performant
method so each call does not need to reauthenticate, is to obtain an access token which can be reused throught out a series
of module invocations.  You can obtain the access token and set it as a fact for use in other modules, like so:

```yaml
---
- collections:
    - pureport.fabric
  tasks:
    - name: Retrieve the access token for an api key and secret
      access_token_info:
        api_key: "{{ api_key }}"
        api_secret: "{{ api_secret }}"
      register: result
    - name: Set the access token as a fact
      set_fact:
        access_token: "{{ result.access_token }}"

    - name: List accounts
      accounts_info:
        api_access_token: "{{ access_token }}"
      register: result
    - debug: var=result
```

### Obtaining and Using Pureport `href`
Many of the Ansible modules provided above have parameters that reference a Pureport object's `href`.  Pureport uses
the `href` link object to build relationships between various other objects, such as Connections belonging to a Network.

An `href` is simply the object's resource path within the Pureport ReST API.

A Pureport Account would have an `href` which is its `id` prefixed with `/accounts/`, like `/accounts/ac-XXXXXXXX`.
Similarly, a Pureport Network would have an `href` which is its `id` prefixed with `/networks/`.
