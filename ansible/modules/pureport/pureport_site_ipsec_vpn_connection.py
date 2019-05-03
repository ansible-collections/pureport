#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_site_ipsec_vpn_connection

short_description: Create, update or delete a Site IPSec VPN connection

version_added: "2.8"

description:
    - "Create, update or delete a Site IPSec VPN connection"

options:
    primary_customer_router_ip:
        description:
            - The VPN's primary router IP address.
        required: true
        type: str
    secondary_customer_router_ip:
        description:
            - The VPN's secondary router IP address (HA).
        required: false
        type: str
    routing_type:
        description:
            - The VPN's routing type.
        required: false
        type: str
        choices: ['ROUTE_BASED_BGP', 'ROUTE_BASED_STATIC', 'POLICY_BASED']
        default: 'ROUTE_BASED_BGP'
    physical_address:
        description:
            - Information about the physical address of the VPN appliance.
        required: false
        type: dict
    ike_version:
        description:
            - The IKE version of the VPN connection.
        required: false
        type: str
        choices: ['V1', 'V2']
        default: 'V2'
    ike_encryption:
        description:
            - The IKE Encryption algorithm
        required: true
        type: str
    ike_integrity:
        description:
            - The IKE Integrity algorithm
            - This is required for IKE version 'V1'.  For IKE 'V2', depending on the IKE Encryption algorithm,
            - this may or may not be required.
        required: false
        type: str
    ike_prf:
        description:
            - The IKE Pseudo-random Function
            - When the IKE version is 'V2', some of the IKE Encryption algorithms require the PRF to be set.
            - Those algorithms also require you to not set the IKE Integrity and therefore 'ike_integrity'
            - and 'ike_prf' are mutually exclusive.
        required: false
        type: str
    ike_dh_group:
        description:
            - The IKE Diffie-Hellman group
        required: true
        type: str
    esp_encryption:
        description:
            - The ESP Encryption algorithm
        required: true
        type: str
    esp_integrity:
        description:
            - The ESP Integrity algorithm
            - Depending on the ESP Encryption algorithm, this may or may not be required.
        required: false
        type: str
    esp_dh_group:
        description:
            - The ESP Diffie-Hellman algorithm
        required: true
        type: str
    primary_key:
        description:
            - The IPSec pre-shared key for the secondary gateway.
        required: false
        type: str
    secondary_key:
        description:
            - The IPSec pre-shared key for the secondary gateway.
        required: false
        type: str
    traffic_selectors:
        description:
            - A list of traffic selectors (e.g dict(customer_side=str, pureport_side=str))
        required: false
        type: list
        default: []
    enable_bgp_password:
        description:
            - Enable a BGP password for the 'ROUTE_BASED_BGP' VPN connection gateways.
        required: false
        type: bool

extends_documentation_fragment:
    - pureport_client
    - pureport_network
    - pureport_wait_for_server
    - pureport_connection_args

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

from functools import partial
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict

from ansible.module_utils.pureport.pureport import \
    get_client_argument_spec, \
    get_network_argument_spec
from ansible.module_utils.pureport.pureport_crud import get_state_argument_spec
from ansible.module_utils.pureport.pureport_connection_crud import \
    get_wait_for_server_argument_spec, \
    get_connection_argument_spec, \
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
        'primary_customer_router_ip',
        'secondary_customer_router_ip',
        'routing_type',
        'physical_address',
        'ike_version',
        'primary_key',
        'secondary_key',
        'traffic_selectors',
        'enable_bgp_password'
    ))
    is_ike_v1 = connection.get('ike_version') == 'V1'
    connection.update([
        (
            'ikeV1' if is_ike_v1 else 'ikeV2',
            dict(
                ike=dict((k[4:], module.params.get(k)) for k in (
                    'ike_encryption',
                    'ike_integrity',
                    'ike_prf' if not is_ike_v1 else None,
                    'ike_dh_group',
                ) if k is not None),
                esp=dict((k[4:], module.params.get(k)) for k in (
                    'esp_encryption',
                    'esp_integrity',
                    'esp_dh_group'
                ))
            )
        )
    ])
    connection.update(dict(
        type='SITE_IPSEC_VPN',
        authType='PSK',
        # TODO(mtraynham): Remove id parsing once we only need to pass href
        location=dict(href=module.params.get('location_href'),
                      id=module.params.get('location_href').split('/')[-1]),
        nat=dict(
            enabled=module.params.get('nat_enabled'),
            mappings=[dict(native_cidr=nat_mapping)
                      for nat_mapping in module.params.get('nat_mappings')]
        )
    ))
    connection = snake_dict_to_camel_dict(connection)
    # Correct naming
    connection.update(dict(
        primaryCustomerRouterIP=connection.pop('primaryCustomerRouterIp'),
        secondaryCustomerRouterIP=connection.pop('secondaryCustomerRouterIp'),
        customerASN=connection.pop('customerAsn'),
        enableBGPPassword=connection.pop('enableBgpPassword')
    ))
    return connection


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_network_argument_spec(True))
    argument_spec.update(get_state_argument_spec())
    argument_spec.update(get_wait_for_server_argument_spec())
    argument_spec.update(get_connection_argument_spec())
    argument_spec.update(
        dict(
            primary_customer_router_ip=dict(type='str', required=True),
            secondary_customer_router_ip=dict(type='str'),
            routing_type=dict(
                type='str',
                choices=[
                    'ROUTE_BASED_BGP',
                    'ROUTE_BASED_STATIC',
                    'POLICY_BASED'
                ],
                default='ROUTE_BASED_BGP'
            ),
            physical_address=dict(type='dict'),
            ike_version=dict(type='str', choices=['V1', 'V2'], default='V2'),
            ike_encryption=dict(type='str', required=True),
            ike_integrity=dict(type='str'),
            ike_prf=dict(type='str'),
            ike_dh_group=dict(type='str', required=True),
            esp_encryption=dict(type='str', required=True),
            esp_integrity=dict(type='str'),
            esp_dh_group=dict(type='str', required=True),
            primary_key=dict(type='str'),
            secondary_key=dict(type='str'),
            traffic_selectors=dict(type='list', default=[]),
            enable_bgp_password=dict(type='bool')
        )
    )
    mutually_exclusive = []
    mutually_exclusive += [
        ['ike_integrity', 'ike_prf']
    ]
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
