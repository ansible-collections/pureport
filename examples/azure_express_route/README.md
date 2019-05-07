## Requirements
A virtualenv with ansible, ansible[azure], azure-cli, and pureport-client.

**Note:** The following will probably throw errors, because of version mismatches with the azure-cli and
ansible[azure] requirements.  You can ignore these.
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Creating an Azure Express Route Connection
This example creates:
- a Azure Express Route Circuit, 
- a Pureport Network, & 
- a Pureport Google Cloud Interconnect Connection

### Running the Example
Add a `group_vars/all.yml` file with the following contents, filling in the parameters where required:

```yaml
azure_user: YOUR ACTIVE DIRECTORY USER NAME
azure_password: YOUR ACTIVE DIRECTORY PASSWORD
azure_subscription_id: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
azure_resource_group: XXXXXXXXXXXXXX
azure_resource_name: A NAME FOR YOUR EXPRESS ROUTE CIRCUIT
azure_location: EXPRESS ROUTE LOCATION  # e.g. West US 2
azure_peering_location: EXPRESS ROUTE PEERING LOCATION  # e.g. Seattle
azure_route_filter_service_communities:  # Used for Microsoft (PUBLIC) Peering, adds Microsoft route propagation
  - #####:#####  # The community attribute (e.g. <Community ASN>:<Community Attribute>)
  # - 12076:53026  # Azure SQL West US 2

pureport_api_key: XXXXXXXXXXXX
pureport_api_secret: XXXXXXXXXXXXXXXX
pureport_account_href: /accounts/ac-XXXXXXXXXXXXXXXX
pureport_network_name: My Simple Azure Network
pureport_connection_name: My Simple Azure Connection
pureport_connection_location_href: /locations/us-sea
pureport_connection_speed: 50
pureport_connection_high_availability: true
pureport_connection_peering_type: PRIVATE  # or PUBLIC
pureport_connection_billing_term: HOURLY

## Set these if you are performing Pureport network/connection updates
# pureport_network_id: network-XXXXXXXXXXXXXXXXXXXXXXXX
# pureport_connection_id: conn-XXXXXXXXXXXXXXXXXXXXXXXX
```

### Some Notes
1. When creating Azure Express Route Circuits, use **Equinix** for the `serviceProviderName`.
2. When updating the Azure Express Route Circuit peering configuration, use **100** for the `vlanId`.
3. When updating the Azure Express Route Circuit peering configuration, use **ARIN** for the `routingRegistryName`.
