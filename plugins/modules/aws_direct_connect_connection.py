#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: aws_direct_connect_connection
short_description: Create, update or delete an AWS Direct Connect connection
description:
    - "Create, update or delete an AWS Direct Connect connection"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    network_href:
        required: true
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
    cloud_service_hrefs:
        description:
            - A list of cloud services for the connection
            - This should be the full 'href' path to the CloudService ReST object (e.g /cloudServices/abc).
        required: false
        type: list
        default: []
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.network
    - pureport.fabric.state
    - pureport.fabric.resolve_existing
    - pureport.fabric.wait_for_server
    - pureport.fabric.connection_args
    - pureport.fabric.peering_connection_args
'''

EXAMPLES = '''
- name: Create a simple PRIVATE AWS Direct Connect connection for a network
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible AWS Direct Connect Connection
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    aws_account_id: XXXXXXXXXXXX
    aws_region: XX-XXXX-#
    wait_for_server: true  # Wait for the server to finish provisioning the connection
  register: result  # Registers the connection as the result

- name: Update the newly created connection with changed properties
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: {{ result.name }}
    speed: 100
    high_availability: {{ result.high_availability }}
    location_href: {{ result.location.href }}
    billing_term: {{ result.billing_term }}
    aws_account_id: {{ result.aws_account_id }}
    aws_region: {{ result.aws_region }}
    wait_for_server: true  # Wait for the server to finish updating the connection
  register: result  # Registers the connection as the result

- name: Delete the newly created connection using the 'absent' state
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    state: absent
    name: {{ result.name }}
    speed: {{ result.speed }}
    high_availability: {{ result.high_availability }}
    location_href: {{ result.location.href }}
    billing_term: {{ result.billing_term }}
    aws_account_id: {{ result.aws_account_id }}
    aws_region: {{ result.aws_region }}
    wait_for_server: true  # Wait for the server to finish deleting the connection

- name: Create a PRIVATE AWS Direct Connect connection with all properties configured
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible AWS Direct Connect
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    aws_account_id: XXXXXXXXXXXX
    aws_region: XX-XXXX-#
    # Optional properties start here
    description: My Ansible managed AWS Direct Connect connection
    peering_type: PRIVATE
    customer_asn: ######
    customer_networks:
      - address: a.b.c.d/x  # A valid CIDR address
        name: My AWS accessible CIDR address
    nat_enabled: true
    nat_mappings:
      - a.b.c.d/x  # A valid CIDR address, likely referencing a Customer Network

- name: Create a PUBLIC AWS Direct Connect connection with all properties configured
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible AWS Direct Connect
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    aws_account_id: XXXXXXXXXXXX
    aws_region: XX-XXXX-#
    # Optional properties start here
    description: My Ansible managed AWS Direct Connect connection
    peering_type: PUBLIC
    cloud_service_hrefs:
      - /cloudServices/aws-XX-XX-XXXX-#
'''

RETURN = '''
connection:
    description: the created, updated, or deleted connection
    type: Connection
'''

from functools import partial
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import \
    camel_dict_to_snake_dict, \
    snake_dict_to_camel_dict

from ..module_utils.pureport_client import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_network_argument_spec
from ..module_utils.pureport_crud import \
    get_state_argument_spec, \
    get_resolve_existing_argument_spec
from ..module_utils.pureport_connection_crud import \
    get_wait_for_server_argument_spec, \
    get_connection_argument_spec, \
    get_cloud_connection_argument_spec, \
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
        'billing_term',
        'customer_asn',
        'customer_networks',
        'aws_account_id',
        'aws_region'
    ))
    connection.update(dict(
        type='AWS_DIRECT_CONNECT',
        peering=dict(type=module.params.get('peering_type')),
        location=dict(href=module.params.get('location_href')),
        cloud_services=[dict(href=cloud_service_href)
                        for cloud_service_href in module.params.get('cloud_service_hrefs')],
        nat=dict(
            enabled=module.params.get('nat_enabled'),
            mappings=[dict(native_cidr=nat_mapping)
                      for nat_mapping in module.params.get('nat_mappings')]
        )
    ))
    connection = snake_dict_to_camel_dict(connection)
    # Correct naming
    connection.update(dict(
        customerASN=connection.pop('customerAsn')
    ))
    return connection


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_network_argument_spec(True))
    argument_spec.update(get_state_argument_spec())
    argument_spec.update(get_resolve_existing_argument_spec())
    argument_spec.update(get_wait_for_server_argument_spec())
    argument_spec.update(get_connection_argument_spec())
    argument_spec.update(get_cloud_connection_argument_spec())
    argument_spec.update(get_peering_connection_argument_spec())
    argument_spec.update(
        dict(
            aws_account_id=dict(type='str', required=True),
            aws_region=dict(type='str', required=True),
            cloud_service_hrefs=dict(type='list', default=[])
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
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
        **camel_dict_to_snake_dict(changed_connection)
    )


if __name__ == '__main__':
    main()
