## Requirements
A virtualenv with ansible, boto3 and the pureport-client.

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Creating an AWS Direct Connect Connection
This example creates:
- an AWS VPC
- an AWS VPC Subnet
- an AWS Virtual Private Gateway
- an AWS VPC Route Table (with VGW route propagation)
- an AWS Direct Connect Gateway
- a Pureport Network
- a Pureport AWS Direct Connect Connection
- an AWS Direct Connect Virtual Interface(s) (VIF)

### Running the Example
Add a `group_vars/all.yml` file with the following contents, filling in the parameters where required:

For Private Peering:
```yaml
aws_access_key: XXXXXXXXXXXXXXXX
aws_secret_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
aws_account_id: YOUR AWS ACCOUNT ID
aws_region: us-west-2
aws_vpc_name: My-Ansible-AWS-VPC
aws_vpc_cidr_block: 10.0.0.0/24
aws_vpc_subnet_cidr: 10.0.0.0/24
aws_vgw_name: My-Ansible-AWS-VGW
aws_vpc_route_table_name: My-Ansible-AWS-RouteTable
aws_direct_connect_gateway_name: My-Ansible-AWS-Gateway
aws_direct_connect_virtual_interface_name: My-Ansible-AWS-VIF

pureport_api_key: XXXXXXXXXXXX
pureport_api_secret: XXXXXXXXXXXXXXXX
pureport_account_href: /accounts/ac-XXXXXXXXXXXXXXXX
pureport_network_name: My Simple AWS Network
pureport_connection_name: My Simple AWS Connection
pureport_connection_location_href: /locations/us-sea
pureport_connection_speed: 50
pureport_connection_high_availability: true
pureport_connection_peering_type: PRIVATE
pureport_connection_billing_term: HOURLY
```

For Public Peering:
```yaml
aws_access_key: XXXXXXXXXXXXXXXX
aws_secret_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
aws_account_id: YOUR AWS ACCOUNT ID
aws_region: us-west-2
aws_direct_connect_virtual_interface_name: My-Ansible-AWS-VIF

pureport_api_key: XXXXXXXXXXXX
pureport_api_secret: XXXXXXXXXXXXXXXX
pureport_account_href: /accounts/ac-XXXXXXXXXXXXXXXX
pureport_network_name: My Simple AWS Network
pureport_connection_name: My Simple AWS Connection
pureport_connection_location_href: /locations/us-sea
pureport_connection_speed: 50
pureport_connection_high_availability: true
pureport_connection_peering_type: PUBLIC
pureport_connection_billing_term: HOURLY
pureport_connection_cloud_service_hrefs:
  - /cloudServices/aws-s3-us-west-2
```