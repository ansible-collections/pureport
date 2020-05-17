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
module: oracle_fast_connect_connection
short_description: Create, update or delete an Oracle Fast Connect connection
description:
    - "Create, update or delete an Oracle Fast Connect connection"
version_added: "2.9"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    cloud_region_id:
        description:
            - The Cloud Region id associated with the Oracle Fast Connect.
            - Only one of 'cloud_region_id' or 'cloud_region_href' should be supplied for this command.
        required: false
        type: str
    cloud_region_href:
        description:
            - The Cloud Region href associated with the Oracle Fast Connect.
            - Only one of 'cloud_region_id' or 'cloud_region_href' should be supplied for this command.
        required: false
        type: str
    primary_ocid:
        description:
            - The Oracle Fast Connect primary OCID associated with the connection.
        required: true
        type: str
    secondary_ocid:
        description:
            - The Oracle Fast Connect secondary OCID associated with the connection.
        required: true
        type: str
    primary_remote_bgp_ip:
        description:
            - The Oracle side primary BGP IP address.
        required: true
        type: str
    primary_pureport_bgp_ip:
        description:
            - The Pureport side primary BGP IP address.
        required: true
        type: str
    secondary_remote_bgp_ip:
        description:
            - The Oracle side secondary BGP IP address.
        required: true
        type: str
    secondary_pureport_bgp_ip:
        description:
            - The Pureport side secondary BGP IP address.
        required: true
        type: str
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.network
    - pureport.fabric.state
    - pureport.fabric.resolve_existing
    - pureport.fabric.wait_for_server
    - pureport.fabric.connection_args
'''

EXAMPLES = '''
- name: Create a simple Oracle Fast Connect connection for a network
  oracle_fast_connect_connection:
    api_base_url: "{{ api_base_url }}"
    api_access_token: "{{ access_token }}"
    network_href: "{{ network_href }}"
    wait_for_server: true
    name: "Test Oracle Fast Connect"
    speed: 1000
    high_availability: true
    location_href: "{{ location_href }}"
    billing_term: HOURLY
    cloud_region_id: "oracle-us-ashburn-1"
    primary_ocid: XXXXXXX
    secondary_ocid: YYYYYYY
    primary_remote_bgp_ip: "192.167.1.1/30"
    primary_pureport_bgp_ip: "192.167.1.2/30"
    secondary_remote_bgp_ip: "192.167.2.1/30"
    secondary_pureport_bgp_ip: "192.167.2.2/30"
    customer_networks:
      - address: 192.167.1.1/32
        name: My Custom Address
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
        'billing_term',
        'customer_networks',
        'primary_ocid',
        'secondary_ocid'
    ))
    connection.update(dict(
        type='ORACLE_FAST_CONNECT',
        high_availability=True,
        location=get_object_link(module, '/locations', 'location_id', 'location_href'),
        cloud_region=get_object_link(module, '/cloudRegions', 'cloud_region_id', 'cloud_region_href'),
        nat=dict(
            enabled=module.params.get('nat_enabled'),
            mappings=[dict(native_cidr=nat_mapping)
                      for nat_mapping in module.params.get('nat_mappings')]
        )
    ))
    connection = snake_dict_to_camel_dict(connection)
    # Correct naming
    connection.update(dict(
        peering=dict(
            type='PRIVATE',
            primaryRemoteBgpIP=module.params.get('primary_remote_bgp_ip'),
            primaryPureportBgpIP=module.params.get('primary_pureport_bgp_ip'),
            secondaryRemoteBgpIP=module.params.get('secondary_remote_bgp_ip'),
            secondaryPureportBgpIP=module.params.get('secondary_pureport_bgp_ip'),
        ),
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
            cloud_region_id=dict(type='str'),
            cloud_region_href=dict(type='str'),
            primary_ocid=dict(type='str', required=True),
            secondary_ocid=dict(type='str', required=True),
            primary_remote_bgp_ip=dict(type='str', required=True),
            primary_pureport_bgp_ip=dict(type='str', required=True),
            secondary_remote_bgp_ip=dict(type='str', required=True),
            secondary_pureport_bgp_ip=dict(type='str', required=True)
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    required_one_of = []
    required_one_of += get_network_mutually_exclusive()
    required_one_of += get_connection_required_one_of()
    required_one_of += [
        ['cloud_region_id', 'cloud_region_href']
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
