#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_google_cloud_interconnect_connection
short_description: Create, update or delete a Google Cloud Interconnect connection
description:
    - "Create, update or delete a Google Cloud Interconnect connection"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    network_href:
        required: true
    primary_pairing_key:
        description:
            - The Google Cloud Interconnect Attachment's primary pairing key.
        required: true
        type: str
    secondary_pairing_key:
        description:
            - The Google Cloud Interconnect Attachment's secondary pairing key (HA).
        required: false
        type: str
extends_documentation_fragment:
    - pureport_client
    - pureport_network
    - pureport_state
    - pureport_resolve_existing
    - pureport_wait_for_server
    - pureport_connection_args
'''

EXAMPLES = '''
- name: Create a simple Google Cloud Interconnect connection for a network
  pureport_aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Google Cloud Interconnect Connection
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    primary_pairing_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX/XX-XXXXXXXX#/1
    secondary_pairing_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX/XX-XXXXXXXX#/2
    wait_for_server: true  # Wait for the server to finish provisioning the connection
  register: result  # Registers the connection as the result

- name: Update the newly created connection with changed properties
  pureport_aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: {{ result.name }}
    speed: 100
    high_availability: {{ result.high_availability }}
    location_href: {{ result.location.href }}
    billing_term: {{ result.billing_term }}
    primary_pairing_key: {{ result.primary_pairing_key }}
    secondary_pairing_key: {{ result.secondary_pairing_key }}
    wait_for_server: true  # Wait for the server to finish updating the connection
  register: result  # Registers the connection as the result

- name: Delete the newly created connection using the 'absent' state
  pureport_aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    state: absent
    name: {{ result.name }}
    speed: {{ result.speed }}
    high_availability: {{ result.high_availability }}
    location_href: {{ result.location.href }}
    billing_term: {{ result.billing_term }}
    primary_pairing_key: {{ result.primary_pairing_key }}
    secondary_pairing_key: {{ result.secondary_pairing_key }}
    wait_for_server: true  # Wait for the server to finish deleting the connection

- name: Create a Google Cloud Interconnect connection with all properties configured
  pureport_aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Google Cloud Interconnect
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    primary_pairing_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX/XX-XXXXXXXX#/1
    secondary_pairing_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX/XX-XXXXXXXX#/2
    # Optional properties start here
    description: My Ansible managed Google Cloud Interconnect connection
    customer_networks:
      - address: a.b.c.d/x  # A valid CIDR address
        name: My AWS accessible CIDR address
    nat_enabled: true
    nat_mappings:
      - a.b.c.d/x  # A valid CIDR address, likely referencing a Customer Network
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

from ansible.module_utils.pureport.pureport import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_network_argument_spec
from ansible.module_utils.pureport.pureport_crud import \
    get_state_argument_spec, \
    get_resolve_existing_argument_spec
from ansible.module_utils.pureport.pureport_connection_crud import \
    get_wait_for_server_argument_spec, \
    get_connection_argument_spec, \
    get_cloud_connection_argument_spec, \
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
        'customer_networks',
        'primary_pairing_key',
        'secondary_pairing_key'
    ))
    connection.update(dict(
        type='GOOGLE_CLOUD_INTERCONNECT',
        # TODO(mtraynham): Remove id parsing once we only need to pass href
        location=dict(href=module.params.get('location_href')),
        nat=dict(
            enabled=module.params.get('nat_enabled'),
            mappings=[dict(native_cidr=nat_mapping)
                      for nat_mapping in module.params.get('nat_mappings')]
        )
    ))
    connection = snake_dict_to_camel_dict(connection)
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
    argument_spec.update(
        dict(
            primary_pairing_key=dict(type='str', required=True),
            secondary_pairing_key=dict(type='str')
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
