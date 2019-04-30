#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_aws_direct_connect_connection

short_description: Create, update or delete an AWS Direct Connect connection

version_added: "2.7"

description:
    - "Create, update or delete an AWS Direct Connect connection"

options:
    api_base_url:
        description:
            - The host url for the Pureport API
        required: false
        type: str
    api_key:
        description:
            - This is the pre-configured API Key for a Pureport Account
        required: true
        type: str
    api_secret:
        description:
            - This is the pre-configured API Secret for a Pureport Account
        required: true
        type: str
    network:
        description:
            - The network for newly created connections
        required: false
        type: dict
    network_id:
        description:
            - The network id for newly created connections
        required: false
        type: str
    id:
        description:
            - The id of the connection (required if updating)
        required: false
        type: str
    name:
        description:
            - The name of the connection
        required: true
        type: str
    description:
        description:
            - A description for the connection
        required: false
        type: str
    speed:
        description:
            - The speed of the connection (Mbps)
        required: true
        type: int
        choices: [50, 100, 200, 300, 400, 500, 1000, 10000]
    high_availability:
        description:
            - If the connection should be high available (2 gateways)
        required: false
        type: bool
    peering_type:
        description:
            - The peering type of the connection
        required: true
        type: str
        choices: ['PRIVATE', 'PUBLIC']
    location:
        description:
            - The Pureport location to connect to
        required: true
        type: dict
    billing_term:
        description:
            - The billing term for the connection
        required: true
        type: str
        choices: ['HOURLY']
    aws_account_id:
        description:
            - The AWS account Id associated with the connection
        required: true
        type: str
    aws_region_id:
        description:
            - The AWS region associated with the connection
        required: true
        type: str
    customer_asn:
        description:
            - A customer ASN for the connection
        required: false
        type: long
    cloud_services:
        description:
            - A list of cloud services for the connection (Link object)
        required: false
        type: list
    customer_networks:
        description:
            - A list of Connection customer networks dict(address=str, name=str)
        required: false
        type: list
    nat:
        description:
            - A NAT configuration
        required: false
        type: dict

extends_documentation_fragment:
    - pureport

author:
    - Matt Traynham (@mtraynham)
'''

EXAMPLES = '''
'''

RETURN = '''
connection:
    description: the created, updated, or deleted connection
    type: Connection
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ec2 import snake_dict_to_camel_dict
from functools import partial

from module_utils.pureport import \
    get_network_argument_spec, \
    get_network_mutually_exclusive
from module_utils.pureport_connection_crud import connection_crud


def construct_connection(module):
    """
    Construct a Connection from the Ansible module arguments
    :param AnsibleModule module: the Ansible module
    :rtype: Connection
    """
    connection = dict((k, module.params.get(k)) for k in (
        'id',
        'name',
        'description',
        'speed',
        'high_availability',
        'location',
        'billing_term',
        'aws_account_id',
        'aws_region_id',
        'cloud_services',
        'customer_networks',
        'nat'
    ))
    connection.update(dict(
        type="AWS_DIRECT_CONNECT",
        peering=dict(type=module.params.get('peering_type'))
    ))
    connection = snake_dict_to_camel_dict(connection)
    return connection


def main():
    argument_spec = dict()
    argument_spec.update(get_network_argument_spec())
    argument_spec.update(
        dict(
            id=dict(type="str"),
            name=dict(type="str", required=True),
            description=dict(type="str"),
            speed=dict(type="int", required=True, choices=[50, 100, 200, 300, 400, 500, 1000, 1000]),
            high_availability=dict(type="bool"),
            location=dict(type="dict", required=True),
            billing_term=dict(type="str", required=True, choices=['HOURLY']),
            aws_account_id=dict(type="str", required=True),
            aws_region_id=dict(type="str", required=True),
            cloud_services=dict(type="list"),
            customer_networks=dict(type="list"),
            nat=dict(type="dict")
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_network_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    # Using partials to fill in the method params
    (changed, changed_connection, connection, existing_connection) = connection_crud(
        module,
        partial(construct_connection, module)
    )
    module.exit_json(changed=changed, connection=changed_connection)


if __name__ == '__main__':
    main()
