#!/usr/bin/python
#
# Copyright: Pureport
# GNU General Public License v3.0+ (see licenses/gpl-3.0-standalone.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
#
from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: port_connection
short_description: Create, update or delete a Port connection
description:
    - "Create, update or delete a Port connection"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    network_href:
        required: true
    primary_port_href:
        description:
            - The primary port href.
        required: true
        type: str
    secondary_port_href:
        description:
            - The secondary port href (required if high_availability is True).
        required: false
        type: str
    primary_customer_vlan:
        description:
            - The primary port's VLAN.
        required: true
        type: int
    secondary_customer_vlan:
        description:
            - The secondary port's VLAN (required if high_availability is True).
        required: false
        type: int
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.network
    - pureport.fabric.state
    - pureport.fabric.resolve_existing
    - pureport.fabric.wait_for_server
    - pureport.fabric.connection_args
'''

EXAMPLES = '''
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
    connection_crud


def construct_connection(module):
    """
    Construct a Connection from the Ansible module arguments
    :param AnsibleModule module: the Ansible module
    :rtype: pureport.api.client.Connection
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
        'primary_customer_vlan',
        'secondary_customer_vlan'
    ))
    connection.update(dict(
        type='PORT',
        location=dict(href=module.params.get('location_href')),
        primary_port=dict(href=module.params.get('primary_port_href')),
        nat=dict(
            enabled=module.params.get('nat_enabled'),
            mappings=[dict(native_cidr=nat_mapping)
                      for nat_mapping in module.params.get('nat_mappings')]
        )
    ))
    if module.params.get('secondary_port_href') is not None:
        connection.update(dict(
            secondary_port=dict(href=module.params.get('secondary_port_href')),
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
    argument_spec.update(
        dict(
            primary_port_href=dict(type='str', required=True),
            secondary_port_href=dict(type='str'),
            primary_customer_vlan=dict(type='int', required=True),
            secondary_customer_vlan=dict(type='int')
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
