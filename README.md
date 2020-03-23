## Pureport Ansible Modules
This is an [Ansible Collection](https://docs.ansible.com/ansible/devel/dev_guide/collections_tech_preview.html) of various 
[library modules](https://docs.ansible.com/ansible/latest/user_guide/modules_intro.html) and 
[roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) which can interact with the 
[Pureport](https://www.pureport.com/) ReST API.

## Installation
This collection is distributed via [ansible-galaxy](https://galaxy.ansible.com/pureport/fabric).

For compatability between Ansible versions, please use the following install methods matching your Ansible version:

| Ansible Version | Pureport Collection Version                                                         | Install Method                                                  |
| --------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 2.8+            | [0.0.9+](https://galaxy.ansible.com/pureport/pureport)                              | `ansible-galaxy collection install pureport.fabric`             |
| 2.7             | [0.0.5 (Galaxy role)](https://galaxy.ansible.com/pureport/pureport_ansible_modules) | `ansible-galaxy role install pureport.pureport_ansible_modules` |

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

It also provides two extra AWS modules:

- `aws_direct_connect_confirm_connection` - Pureport creates [Hosted Direct Connections](https://docs.aws.amazon.com/directconnect/latest/UserGuide/accept-hosted-connection.html)
which need to be confirmed by the customer when created.  This requires a user to go into the AWS Console and "Approve" the connection.  Alternatively,
this module does that for you using credentials in a similar fashion as other AWS modules and boto3.
- `pr_48711_aws_direct_connect_virtual_interface` - There is an outstanding PR which adds `direct_connect_id` to the Ansible provided 
`aws_direct_connect_virtual_interface` module.  This is required to create Virtual Interfaces with Direct Connect Gateways. 
That PR is [here](https://github.com/ansible/ansible/pull/48711).  This module just duplicates that effort here so it can be used.
For general information about this module, see the [Ansible docs](https://docs.ansible.com/ansible/2.8/modules/aws_direct_connect_virtual_interface_module.html).
  - **NOTE**: This will likely be removed in the future.
  
### Roles
It also provides the following roles you can use to create connections and their full infrastructure:

- `pureport_aws_direct_connect` - Depending on the peering type (PUBLIC/PRIVATE), this will generate:
  - an AWS VPC (PRIVATE only)
  - an AWS VPC Subnet (PRIVATE only)
  - an AWS Virtual Private Gateway (PRIVATE only)
  - an AWS VPC Route Table (with VGW route propagation; PRIVATE only)
  - an AWS Direct Connect Gateway
  - a Pureport Network
  - a Pureport AWS Direct Connect Connection
  - an AWS Direct Connect Virtual Interface(s) (VIF)
- `pureport_azure_express_route` - Depending on the peering type (PUBLIC/PRIVATE), this will generate:
  - an Azure Virtual Network (with 2 subnets; PRIVATE only)
  - an Azure Public IP Address (PRIVATE only)
  - an Azure Virtual Network Gateway (PRIVATE only)
  - an Azure Express Route Circuit
  - an Azure Virtual Network Gateway to Express Route Connection (PRIVATE only)
  - an Azure Route Filter (PUBLIC only)
  - a Pureport Network
  - a Pureport Azure Express Route Connection
  - Private Express Route Peering (PRIVATE only)
  - Microsoft Express Route Peering (PUBLIC only)
- `pureport_google_cloud_interconnect`
  - a GCP Network
  - a GCP Router(s)
  - a GCP Interconnect Attachment(s)
  - a Pureport Network
  - a Pureport Google Cloud Interconnect Connection
- `pureport_site_ipsec_vpn`
  - a Pureport Network
  - a Pureport Site IPsec VPN Connection

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

ansible-doc pureport.fabric.aws_direct_connect_confirm_connection
ansible-doc pureport.fabric.pr_48711_aws_direct_connect_virtual_interface
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

ansible-doc pureport.fabric.aws_direct_connect_confirm_connection -s
ansible-doc pureport.fabric.pr_48711_aws_direct_connect_virtual_interface -s
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

### Ansible 2.9/Pureport 0.0.9 Module Rename
The 0.0.9 release has renamed all the modules to have shortner names, while using the collection namespace.  For 
backwards-compatability all existing module names have been simply symlinked to their new module and should work
as they previously had.

For reference the names have been changed from/to:

| Name                                  | Ansible 2.8/Pureport 0.0.8 Name                |
|---------------------------------------|------------------------------------------------|
|`access_token_info`                    |`pureport_access_token_fact`                    |
|`locations_info`                       |`pureport_location_facts`                       |
|`facilities_info`                      |`pureport_facility_facts`                       |
|`options_info`                         |`pureport_option_facts`                         |
|`cloud_regions_info`                   |`pureport_cloud_region_facts`                   |
|`cloud_services_info`                  |`pureport_cloud_service_facts`                  |
|`accounts_info`                        |`pureport_account_facts`                        |
|`supported_connections_info`           |`pureport_supported_connection_facts`           |
|`supported_ports_info`                 |`pureport_supported_port_facts`                 |
|`ports_info`                           |`pureport_port_facts`                           |
|`port`                                 |`pureport_port`                                 |
|`networks_info`                        |`pureport_network_facts`                        |
|`network`                              |`pureport_network`                              |
|`connections_info`                     |`pureport_connection_facts`                     |
|`aws_direct_connect_connection`        |`pureport_aws_direct_connect_connection`        |
|`azure_express_route_connection`       |`pureport_azure_express_route_connection`       |
|`google_cloud_interconnect_connection` |`pureport_google_cloud_interconnect_connection` |
|`port_connection`                      |`pureport_port_connection`                      |
|`site_ipsec_vpn_connection`            |`pureport_site_ipsec_vpn_connection`            |

## Examples
There are various examples on how to use these modules in the [examples directory](examples/README.md).
