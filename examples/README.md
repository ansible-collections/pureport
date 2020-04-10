## Examples

This directory contains various playbook examples using the roles provided by the pureport.fabric
collection.

- [pureport_aws_direct_connect_private.yml](pureport_aws_direct_connect_private.yml) - Create a single private AWS connection and infrastructure
- [pureport_aws_direct_connect_public.yml](pureport_aws_direct_connect_public.yml) - Create a single public AWS connection and infrastructure
- [pureport_azure_express_route_private.yml](pureport_azure_express_route_private.yml) - Create a single private Azure connection and infrastructure
- [pureport_azure_express_route_public.yml](pureport_azure_express_route_public.yml) - Create a single public Azure connection and infrastructure
- [pureport_google_cloud_interconnect.yml](pureport_google_cloud_interconnect.yml) - Create a single Google connection and infrastructure
- [pureport_site_ipsec_vpn.yml.yml](pureport_site_ipsec_vpn.yml) - Create a Site IPSec VPN connection
- [main.yml](main.yml) - Runs all the above examples in a single Pureport network

### Ansible Meetup Example
Pureport hosted an Ansible meetup on 8/28/19.  The demo playbook [ansible_meetup.yml](ansible_meetup.yml) ([ansible_meetup_teardown.yml](ansible_meetup_teardown.yml)) and extra 
roles ([aws_ec2_instance](roles/aws_ec2_instance/tasks/main.yml) and [google_vm_instance](roles/google_vm_instance/tasks/main.yml))
have been duplicated here for you to run.

The Ansible Meetup example uses the existing roles here to spin up AWS VPC and Google Virtual Network infrastructures, put a single
VM instance within both of them and provides SSH access publicly and trigger ping calls between the two VMs privately.

The meetup presentation has been copied here to [ansible_meetup.pdf](ansible_meetup.pdf).  If you would like to view the original repository,
that can be found [here](https://github.com/pureport/pureport-ansible-meetup).

### Requirements
There is some configuration required to run these examples.

A virtualenv with ansible[azure], boto3, google-auth, and pureport-client
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

- A valid Service Account private key file (json format).  This is obtained from the 
[Google Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) page.

*group_vars/all.yml*
```yaml
aws_access_key: ###############
aws_secret_key: ##########################################
aws_account_id: ###############

azure_user: YOUR AZURE USER NAME
azure_password: YOUR AZURE PASSWORD
azure_subscription_id: YOUR AZURE SUBSCRIPTION ID
azure_resource_group: YOUR AZURE RESOURCE GROUP

gcp_service_account_file: YOUR SERVICE ACCOUNT FILE PATH HERE
gcp_project: YOUR GCP PROJECT NAME

pureport_account_href: /accounts/ac-XXXXXXXXXXXXXXXX
pureport_api_key: XXXXXXXXXXXX
pureport_api_secret: XXXXXXXXXXXXXXXX
pureport_network_name: My Simple Network
```
