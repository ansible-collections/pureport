## Pureport Ansible Modules
This is an [Ansible Collection](https://docs.ansible.com/ansible/devel/dev_guide/collections_tech_preview.html) of various 
[library modules](https://docs.ansible.com/ansible/2.8/user_guide/modules_intro.html) and 
[roles](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_reuse_roles.html) which can interact with the 
[Pureport](https://www.pureport.com/) ReST API.

## Installation
This collection is distributed via [ansible-galaxy](https://galaxy.ansible.com/).

```bash
mazer install pureport.pureport
```

Because this is based on the newer Ansible Collections format, Ansible 2.8+ is required.  Please use version 0.0.5 of
[pureport.pureport_ansible_modules](https://galaxy.ansible.com/pureport/pureport_ansible_modules) if you are using Anisble < 2.8.

```bash
ansible-galaxy install pureport.pureport_ansible_modules
```

### Modules
It provides the following modules you can use in your own roles:

- `pureport_access_token_fact` - Obtain an OAuth access token which can be used as the `api_access_token` param 
  for all other modules in lieu of passing them the `api_key`/`api_secret`.  This allows other modules to skip their own retrieval 
  of the `access_token`, further reducing the number of API calls and execution time. 
- `pureport_location_facts` - used to list a set of locations
- `pureport_facility_facts` - used to list a set of facilities
- `pureport_option_facts` - used to list a set of enum options used for creating connections
- `pureport_cloud_region_facts` - used to list a set of cloud region objects for various connection types
- `pureport_cloud_service_facts` - used to list a set of cloud service objects for public connections
- `pureport_account_facts` - used to list available accounts for an API key
- `pureport_supported_connection_facts` - used to list available supported connections for an account
- `pureport_supported_port_facts` - used to list available supported ports
- `pureport_port_facts` - used to list ports for an account
- `pureport_port` - used to create/update/delete a port
- `pureport_network_facts` - used to list a set of networks
- `pureport_network` - used to create/update/delete a network
- `pureport_connection_facts` - used to list a set of connections
- `pureport_aws_direct_connect_connection` - used to create/update/delete a Pureport AWS connection
- `pureport_azure_express_route_connection` - used to create/update/delete a Pureport Azure Express Route connection
- `pureport_google_cloud_interconnect_connection` - used to create/update/delete a Pureport Google Cloud Interconnect connection
- `pureport_port_connection` - used to create/update/delete a Pureport Port connection
- `pureport_site_ipsec_vpn_connection` - used to create/update/delete a Pureport Site IPSec VPN connection

It also provides two extra AWS modules:

- `aws_direct_connect_confirm_connection` - Pureport creates [Hosted Direct Connections](https://docs.aws.amazon.com/directconnect/latest/UserGuide/accept-hosted-connection.html)
which need to be confirmed by the customer when created.  This requires a user to go into the AWS Console and "Approve" the connection.  Alternatively,
this module does that for you using credentials in a similar fashion as other AWS modules and boto3.
- `pr_48711_aws_direct_connect_virtual_interface` - There is an outstanding PR which adds `direct_connect_id` to the Ansible provided 
`aws_direct_connect_virtual_interface` module.  This is required to create Virtual Interfaces with Direct Connect Gateways. 
That PR is [here](https://github.com/ansible/ansible/pull/48711).  This module just duplicates that effort here so it can be used.
For general information about this module, see the [Ansible docs](https://docs.ansible.com/ansible/2.8/modules/aws_direct_connect_virtual_interface_module.html).
  - **NOTE**: This will likely be removed in the future.
- `pr_60938_gcp_compute_interconnect_attachment` - There is an outstanding PR which adds `admin_enabled` to the Ansible provided
`gcp_compute_interconnect_attachment`.  This is required to "Pre-Activate" PARTNER type Google Cloud Interconnect Attachments.
That PR is [here](https://github.com/ansible/ansible/pull/60938) .  This module just duplicates that effort here so it can be used.
For general information about this module, see the [Ansible docs](https://docs.ansible.com/ansible/latest/modules/gcp_compute_interconnect_attachment_module.html).
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
ansible-doc pureport.pureport.pureport_access_token_fact
ansible-doc pureport.pureport.pureport_location_facts
ansible-doc pureport.pureport.pureport_facility_facts
ansible-doc pureport.pureport.pureport_option_facts
ansible-doc pureport.pureport.pureport_cloud_region_facts
ansible-doc pureport.pureport.pureport_cloud_service_facts
ansible-doc pureport.pureport.pureport_account_facts
ansible-doc pureport.pureport.pureport_supported_connection_facts
ansible-doc pureport.pureport.pureport_supported_port_facts
ansible-doc pureport.pureport.pureport_port_facts
ansible-doc pureport.pureport.pureport_port
ansible-doc pureport.pureport.pureport_network_facts
ansible-doc pureport.pureport.pureport_network
ansible-doc pureport.pureport.pureport_connection_facts
ansible-doc pureport.pureport.pureport_aws_direct_connect_connection
ansible-doc pureport.pureport.pureport_azure_express_route_connection
ansible-doc pureport.pureport.pureport_google_cloud_interconnect_connection
ansible-doc pureport.pureport.pureport_port_connection
ansible-doc pureport.pureport.pureport_site_ipsec_vpn_connection

ansible-doc pureport.pureport.aws_direct_connect_confirm_connection
ansible-doc pureport.pureport.pr_48711_aws_direct_connect_virtual_interface
ansible-doc pureport.pureport.pr_60938_gcp_compute_interconnect_attachment
```

Also dump a snippet of what invoking a module requires:
```bash
ansible-doc pureport.pureport.pureport_access_token_fact -s
ansible-doc pureport.pureport.pureport_facility_facts -s
ansible-doc pureport.pureport.pureport_location_facts -s
ansible-doc pureport.pureport.pureport_option_facts -s
ansible-doc pureport.pureport.pureport_cloud_region_facts -s
ansible-doc pureport.pureport.pureport_cloud_service_facts -s
ansible-doc pureport.pureport.pureport_account_facts -s
ansible-doc pureport.pureport.pureport_supported_connection_facts -s
ansible-doc pureport.pureport.pureport_supported_port_facts -s
ansible-doc pureport.pureport.pureport_port_facts -s
ansible-doc pureport.pureport.pureport_port -s
ansible-doc pureport.pureport.pureport_network_facts -s
ansible-doc pureport.pureport.pureport_network -s
ansible-doc pureport.pureport.pureport_connection_facts -s
ansible-doc pureport.pureport.pureport_aws_direct_connect_connection -s
ansible-doc pureport.pureport.pureport_azure_express_route_connection -s
ansible-doc pureport.pureport.pureport_google_cloud_interconnect_connection -s
ansible-doc pureport.pureport.pureport_port_connection -s
ansible-doc pureport.pureport.pureport_site_ipsec_vpn_connection -s

ansible-doc pureport.pureport.aws_direct_connect_confirm_connection -s
ansible-doc pureport.pureport.pr_48711_aws_direct_connect_virtual_interface -s
ansible-doc pureport.pureport.pr_60938_gcp_compute_interconnect_attachment -s
```

### Obtaining and Using Pureport `href`
Many of the Ansible modules provided above have parameters that reference a Pureport object's `href`.  Pureport uses
the `href` link object to build relationships between various other objects, such as Connections belonging to a Network.

An `href` is simply the object's resource path within the Pureport ReST API.

A Pureport Account would have an `href` which is its `id` prefixed with `/accounts/`, like `/accounts/ac-XXXXXXXX`.
Similarly, a Pureport Network would have an `href` which is its `id` prefixed with `/networks/`.

## Examples
There are various examples on how to use these modules in the [examples directory](examples/README.md).
