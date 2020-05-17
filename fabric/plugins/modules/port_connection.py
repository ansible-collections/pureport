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
    primary_port_id:
        description:
            - The primary port id.
            - Only one of 'primary_port_id' or 'primary_port_href' can be supplied for this command.
        required: false
        type: str
    primary_port_href:
        description:
            - The primary port href.
            - Only one of 'primary_port_id' or 'primary_port_href' can be supplied for this command.
        required: false
        type: str
    secondary_port_id:
        description:
            - The secondary port id (required if high_availability is True).
            - Only one of 'secondary_port_id' or 'secondary_port_href' can be supplied for this command.
        required: false
        type: str
    secondary_port_href:
        description:
            - The secondary port href (required if high_availability is True).
            - Only one of 'secondary_port_id' or 'secondary_port_href' can be supplied for this command.
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
    type: dict
    returned: always
'''

from functools import partial
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import \
    camel_dict_to_snake_dict, \
    snake_dict_to_camel_dict
from traceback import format_exc
try:
    from pureport.exception.api import ClientHttpException
except ImportError:
    ClientHttpException = None

from ..module_utils.pureport_client import \
    get_object_link, \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_network_argument_spec, \
    get_network_mutually_exclusive
from ..module_utils.pureport_crud import \
    get_state_argument_spec, \
    get_resolve_existing_argument_spec
from ..module_utils.pureport_connection_crud import \
    get_wait_for_server_argument_spec, \
    get_connection_argument_spec, \
    get_connection_required_one_of, \
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
        location=get_object_link(module, '/locations', 'location_id', 'location_href'),
        primary_port=get_object_link(module, '/ports', 'primary_port_id', 'primary_port_href'),
        nat=dict(
            enabled=module.params.get('nat_enabled'),
            mappings=[dict(native_cidr=nat_mapping)
                      for nat_mapping in module.params.get('nat_mappings')]
        )
    ))
    secondary_port = get_object_link(module, '/ports', 'secondary_port_id', 'secondary_port_href')
    if secondary_port is not None:
        connection.update(dict(
            secondary_port=secondary_port,
        ))
    connection = snake_dict_to_camel_dict(connection)
    # Correct naming
    connection.update(dict(
        customerASN=connection.pop('customerAsn'),
        tags=module.params.get('tags')
    ))
    return connection


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_network_argument_spec())
    argument_spec.update(get_state_argument_spec())
    argument_spec.update(get_resolve_existing_argument_spec())
    argument_spec.update(get_wait_for_server_argument_spec())
    argument_spec.update(get_connection_argument_spec())
    argument_spec.update(get_cloud_connection_argument_spec())
    argument_spec.update(
        dict(
            primary_port_id=dict(type='str'),
            primary_port_href=dict(type='str'),
            secondary_port_id=dict(type='str'),
            secondary_port_href=dict(type='str'),
            primary_customer_vlan=dict(type='int', required=True),
            secondary_customer_vlan=dict(type='int')
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    mutually_exclusive += [
        ['secondary_port_id', 'secondary_port_href']
    ]
    required_one_of = []
    required_one_of += get_network_mutually_exclusive()
    required_one_of += get_connection_required_one_of()
    required_one_of += [
        ['primary_port_id', 'primary_port_href']
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        required_one_of=required_one_of
    )
    # Using partials to fill in the method params
    try:
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
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
