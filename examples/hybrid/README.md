## Requirements
A virtualenv with ansible, boto3, google-auth, and pureport-client
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

- A valid Service Account private key file (json format).  This is obtained from the 
[Google Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) page.


## Creating a Google Cloud Interconnect Connection
This example creates:
- a Private Pureport AWS Connection
- a Public Pureport AWS Connection
- a Pureport Google Cloud Interconnect Connection
- a Pureport Site IPSec VPN Connection

### Running the Example
Add a `group_vars/all.yml` file with the following contents, filling in the parameters where required:

```yaml
aws_access_key: ###############
aws_secret_key: ###################################
aws_account_id: ###########

gcp_service_account_file: YOUR SERVICE ACCOUNT FILE PATH HERE
gcp_project: YOUR GCP PROJECT NAME

pureport_api_key: XXXXXXXXXXXX
pureport_api_secret: XXXXXXXXXXXXXXXX
pureport_account_href: /accounts/ac-XXXXXXXXXXXXXXXX
pureport_network_name: My Simple Network
```
