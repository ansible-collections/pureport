## Requirements
A virtualenv with ansible[azure] and the pureport-client.

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Creating an Azure Express Route Connection
For Private peering, this example creates:
- an Azure Virtual Network (with 2 subnets)
- an Azure Public IP Address
- an Azure Virtual Network Gateway
- an Azure Express Route Circuit
- an Azure Virtual Network Gateway to Express Route Connection
- a Pureport Network
- a Pureport Azure Express Route Connection
- Private Express Route Peering

For Microsoft peering, this example creates:
- an Azure Express Route Circuit
- an Azure Route Filter
- a Pureport Network
- a Pureport Azure Express Route Connection
- Microsoft Express Route Peering

### Running the Example
Add a `group_vars/all.yml` file with the following contents, filling in the parameters where required.

For Private Peering:
```yaml
azure_user: YOUR ACTIVE DIRECTORY USER NAME
azure_password: YOUR ACTIVE DIRECTORY PASSWORD
azure_subscription_id: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
azure_resource_group: XXXXXXXXXXXXXX
azure_location: westus2
azure_virtual_network_name: ansibleVirtualNetwork
azure_virtual_network_prefixes_cidr:
  - "10.0.0.0/16"
azure_virtual_network_default_subnet: "10.1.0.0/24"
azure_virtual_network_gateway_subnet: "10.1.1.0/24"
azure_public_ip_address_name: ansiblePublicIpAddress
azure_virtual_network_gateway_name: ansibleVirtualNetworkGateway
azure_express_route_circuit_name: ansibleExpressRouteCircuit
azure_express_route_circuit_peering_location: Seattle
azure_virtual_network_express_route_circuit_connection_name: ansibleExpressRouteConnection

pureport_api_key: XXXXXXXXXXXX
pureport_api_secret: XXXXXXXXXXXXXXXX
pureport_account_href: /accounts/ac-XXXXXXXXXXXXXXXX
pureport_network_name: My Simple Azure Network
pureport_connection_name: My Simple Azure Connection
pureport_connection_location_href: /locations/us-sea
pureport_connection_speed: 50
pureport_connection_high_availability: true
pureport_connection_peering_type: PRIVATE
pureport_connection_billing_term: HOURLY
```

For Microsoft Peering:
```yaml
azure_user: YOUR ACTIVE DIRECTORY USER NAME
azure_password: YOUR ACTIVE DIRECTORY PASSWORD
azure_subscription_id: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
azure_resource_group: XXXXXXXXXXXXXX
azure_location: westus2
azure_express_route_circuit_name: ansibleExpressRouteCircuit
azure_express_route_circuit_peering_location: Seattle
azure_route_filter_name: ansibleRouteFilter
azure_route_filter_rule_name: ansibleRouteFilterRule
azure_route_filter_rule_service_communities:
  - 12076:53026  # Azure SQL West US 2

pureport_api_key: XXXXXXXXXXXX
pureport_api_secret: XXXXXXXXXXXXXXXX
pureport_account_href: /accounts/ac-XXXXXXXXXXXXXXXX
pureport_network_name: My Simple Azure Network
pureport_connection_name: My Simple Azure Connection
pureport_connection_location_href: /locations/us-sea
pureport_connection_speed: 50
pureport_connection_high_availability: true
pureport_connection_peering_type: PUBLIC
pureport_connection_billing_term: HOURLY
```

Run it:
```bash
ansible-playbook site.yml
```

### Some Notes
1. When creating Azure Express Route Circuits, use **Equinix** for the `serviceProviderName`.
2. When updating the Azure Express Route Circuit peering configuration, use **100** for the `vlanId`.
3. When updating the Azure Express Route Circuit peering configuration, use **ARIN** for the `routingRegistryName`.

There is an [open issue](https://github.com/ansible/ansible/issues/56356) with Ansible that may mark some of these
tasks as changed on subsequent runs when they really are not.

Also, the peering steps may signal that they have changed for two reasons listed below.  These are also related to the bug
described above and how the `azure_rm_resource` module detects idempotency changes.
- The server does not return the `sharedKey` back, so the step will always be marked as `changed`.
- Also, there doesn't seem to be a proper way to [cast int's](https://github.com/ansible/ansible/issues/30366), so the ASN
  will also signal a change because Ansible treats it as a string, but the server is returning a int/long.
