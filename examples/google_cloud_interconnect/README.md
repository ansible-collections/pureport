## Requirements
A virtualenv with ansible, google-auth, and pureport-client
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

- A valid Service Account private key file (json format).  This is obtained from the 
[Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) page.


## Creating a Google Cloud Interconnect Connection
This example creates:
- a GCP Network, 
- a GCP Router(s), 
- a GCP Interconnect Attachment(s), 
- a Pureport Network, & 
- a Pureport Google Cloud Interconnect Connection

### Running the Example
Add a `group_vars/all.yml` file with the following contents, filling in the parameters where required:

```yaml
gcp_service_account_file: YOUR SERVICE ACCOUNT FILE PATH HERE
gcp_project: YOUR GCP PROJECT NAME
gcp_network_prefix: A PREFIX TO USE FOR ALL THE GCP OBJECTS  # keep it somewhat short, GCP has 64 character limit on some of these things
gcp_region: YOUR GCP REGION  # e.g us-west-2

pureport_api_key: XXXXXXXXXXXX
pureport_api_secret: XXXXXXXXXXXXXXXX
pureport_account_href: /accounts/ac-XXXXXXXXXXXXXXXX
pureport_network_name: My Simple Google Cloud Network
pureport_connection_name: My Simple Google Cloud Connection
pureport_connection_location_href: /locations/us-sea
pureport_connection_speed: 50
pureport_connection_billing_term: HOURLY

## Set this if you want to turn on high availability
# pureport_connection_high_availability: true

## Set these if you are performing Pureport network/connection updates
# pureport_network_id: network-XXXXXXXXXXXXXXXXXXXXXXXX
# pureport_connection_id: conn-XXXXXXXXXXXXXXXXXXXXXXXX
```

### Some Notes
1. When creating GCP Routers, always use **16550** for the `bgp.asn`.
2. When creating GCP Interconnect Attachments, always use **PARTNER** for the `type`.
