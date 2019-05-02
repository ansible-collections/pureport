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
    aws_account_id:
        description:
            - The AWS account Id associated with the connection
        required: true
        type: str
    aws_region:
        description:
            - The AWS region associated with the connection
        required: true
        type: str
    cloud_services:
        description:
            - A list of cloud services for the connection (Link object)
        required: false
        type: list

extends_documentation_fragment:
    - pureport_client
    - pureport_network
    - pureport_wait_for_server
    - pureport_connection_args
    - pureport_peering_connection_args

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

from ansible.module_utils.pureport.pureport import \
    get_client_argument_spec, \
    get_network_argument_spec, \
    get_network_mutually_exclusive
from ansible.module_utils.pureport.pureport_crud import get_state_argument_spec
from ansible.module_utils.pureport.pureport_connection_crud import \
    get_wait_for_server_argument_spec, \
    get_connection_argument_spec, \
    get_peering_connection_argument_spec, \
    connection_crud


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
        'aws_region',
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
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_network_argument_spec())
    argument_spec.update(get_state_argument_spec())
    argument_spec.update(get_wait_for_server_argument_spec())
    argument_spec.update(get_connection_argument_spec())
    argument_spec.update(get_peering_connection_argument_spec())
    argument_spec.update(
        dict(
            aws_account_id=dict(type="str", required=True, no_log=True),
            aws_region=dict(type="str", required=True),
            cloud_services=dict(type="list", no_log=True)
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_network_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    # Using partials to fill in the method params
    (
        changed,
        changed_connection,
        argument_connection,
        existing_connection
    ) = connection_crud(
        module,
        partial(construct_connection, module)
    )
    module.exit_json(
        changed=changed,
        connection=changed_connection,
        argument_connection=argument_connection,
        existing_connection=existing_connection
    )


if __name__ == '__main__':
    main()
