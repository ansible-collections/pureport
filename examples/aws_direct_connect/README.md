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
- an AWS Virtual Private Gateway
- an AWS Direct Connect Gateway
- a Pureport Network
- a Pureport AWS Direct Connect Connection
- an AWS Direct Connect Virtual Interface (VIF)

### Running the Example
Add a `group_vars/all.yml` file with the following contents, filling in the parameters where required:

```yaml
aws_access_key: XXXXXXXXXXXXXXXX
aws_secret_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
aws_account_id: YOUR AWS ACCOUNT ID
aws_region: THE AWS REGION   # us-west-2
aws_vpc_name: My-Ansible-AWS-VPC
aws_vpc_cidr_block: 10.0.0.0/24
aws_vgw_name: My-Ansible-AWS-VGW
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
pureport_connection_peering_type: PRIVATE  # or PUBLIC
pureport_connection_billing_term: HOURLY
pureport_connection_cloud_service_hrefs:
  - /cloudServices/aws-s3-us-west-2

## Set these if you are performing Pureport network/connection updates
# pureport_network_id: network-XXXXXXXXXXXXXXXXXXXXXXXX
# pureport_connection_id: conn-XXXXXXXXXXXXXXXXXXXXXXXX
```
