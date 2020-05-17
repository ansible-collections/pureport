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
module: site_ipsec_vpn_connection
short_description: Create, update or delete a Site IPSec VPN connection
description:
    - "Create, update or delete a Site IPSec VPN connection"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
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
        suboptions:
            street:
                description:
                    - The street address
                required: false
                type: str
            city:
                description:
                    - The city
                required: false
                type: str
            state:
                description:
                    - The state
                required: false
                type: str
            postalCode:
                description:
                    - The postal code
                required: false
                type: str
            country:
                description:
                    - The country
                required: false
                type: str
            geoCoordinates:
                description:
                    - A dict representing the geocoordinates of a location
                required: false
                type: dict
                suboptions:
                    latitude:
                        description:
                            - The latitude
                        required: false
                        type: float
                    longitude:
                        description:
                            - The logitude
                        required: false
                        type: float
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
        required: false
        type: str
        choices: ['NULL', 'AES_128', 'AES_192', 'AES_256', 'AES_128_CTR', 'AES_192_CTR',
                  'AES_256_CTR', 'AES_128_GCM_64', 'AES_192_GCM_64', 'AES_256_GCM_64', 'AES_128_GCM_96',
                  'AES_192_GCM_96', 'AES_256_GCM_96', 'AES_128_GCM_128', 'AES_192_GCM_128', 'AES_256_GCM_128']
        default: 'AES_128'
    ike_integrity:
        description:
            - The IKE Integrity algorithm
            - This is required for IKE version 'V1'.  For IKE 'V2', depending on the IKE Encryption algorithm,
            - this may or may not be required.
        required: false
        type: str
        choices: ['MD5_HMAC', 'SHA1_HMAC', 'SHA256_HMAC', 'SHA384_HMAC', 'SHA512_HMAC', 'AES_XCBC']
    ike_prf:
        description:
            - The IKE Pseudo-random Function
            - When the IKE version is 'V2', some of the IKE Encryption algorithms require the PRF to be set.
            - Those algorithms also require you to not set the IKE Integrity and therefore 'ike_integrity'
            - and 'ike_prf' are mutually exclusive.
        required: false
        type: str
        choices: ['MD5', 'SHA_1', 'AES_XCBC', 'SHA_256', 'SHA_384', 'SHA_512']
    ike_dh_group:
        description:
            - The IKE Diffie-Hellman group
        required: false
        type: str
        choices: ['MODP_1024', 'MODP_1536', 'MODP_2048', 'MODP_3072', 'MODP_4096', 'MODP_6144',
                  'MODP_8192', 'ECP_192', 'ECP_224', 'ECP_256', 'ECP_384', 'ECP_521']
        default: 'MODP_2048'
    esp_encryption:
        description:
            - The ESP Encryption algorithm
        required: false
        type: str
        choices: ['NULL', 'AES_128', 'AES_192', 'AES_256', 'AES_128_CTR', 'AES_192_CTR', 'AES_256_CTR',
                  'AES_128_GCM_64', 'AES_192_GCM_64', 'AES_256_GCM_64', 'AES_128_GCM_96', 'AES_192_GCM_96',
                  'AES_256_GCM_96', 'AES_128_GCM_128', 'AES_192_GCM_128', 'AES_256_GCM_128', 'AES_128_GMAC',
                  'AES_192_GMAC', 'AES_256_GMAC']
        default: 'AES_128'
    esp_integrity:
        description:
            - The ESP Integrity algorithm
            - Depending on the ESP Encryption algorithm, this may or may not be required.
        required: false
        type: str
        choices: ['MD5_HMAC', 'SHA1_HMAC', 'SHA256_HMAC', 'SHA384_HMAC', 'SHA512_HMAC', 'AES_XCBC']
    esp_dh_group:
        description:
            - The ESP Diffie-Hellman algorithm
        required: false
        type: str
        choices: ['MODP_1024', 'MODP_1536', 'MODP_2048', 'MODP_3072', 'MODP_4096', 'MODP_6144',
                  'MODP_8192', 'ECP_192', 'ECP_224', 'ECP_256', 'ECP_384', 'ECP_521']
        default: 'MODP_2048'
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
            - A list of traffic selectors
        required: false
        type: list
        default: []
        elements: dict
        suboptions:
            customer_side:
                description:
                    - A CIDR (a.b.c.d/n) address representing a subnet on the customer side.
                    - This should reference a Customer Network, but it doesn't have to.
                required: true
                type: str
            pureport_side:
                description:
                    - A CIDR (a.b.c.d/n) address representing a subnet on the pureport side.
                    - This should reference the customer_networks of another connection in the contained Network,
                    - or it should reference the connections NAT mapped natCidr field if the connection had NAT enabled.
    enable_bgp_password:
        description:
            - Enable a BGP password for the 'ROUTE_BASED_BGP' VPN connection gateways.
        required: false
        type: bool
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.network
    - pureport.fabric.state
    - pureport.fabric.resolve_existing
    - pureport.fabric.wait_for_server
    - pureport.fabric.connection_args
'''

EXAMPLES = '''
- name: Create a simple ROUTE_BASED_BGP Site IPSec VPN connection for a network
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Site IPSec VPN Connection
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    primary_customer_router_ip: a.b.c.d  # A valid Public IP Address
    secondary_customer_router_ip: a.b.c.d  # A valid Public IP Address
    routing_type: ROUTE_BASED_BGP
    customer_asn: ######
    ike_version: V2
    ike_encryption: AES_128
    ike_integrity: SHA256_HMAC
    ike_dh_group: MODP_2048
    esp_encryption: AES_128
    esp_integrity: SHA256_HMAC
    esp_dh_group: MODP_2048
    wait_for_server: true  # Wait for the server to finish provisioning the connection
  register: result  # Registers the connection as the result

- name: Update the newly created connection with changed properties
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: "{{ result.name }}"
    speed: 100
    high_availability: "{{ result.high_availability }}"
    location_href: "{{ result.location.href }}"
    billing_term: "{{ result.billing_term }}"
    primary_customer_router_ip: "{{ result.primary_customer_router_ip }}"
    secondary_customer_router_ip: "{{ result.secondary_customer_router_ip }}"
    routing_type: "{{ result.routing_type }}"
    customer_asn: "{{ result.customer_asn }}"
    ike_version: "{{ result.ike_version }}"
    ike_encryption: "{{ result.ike_v2.ike.encryption }}"
    ike_integrity: "{{ result.ike_v2.ike.integrity }}"
    ike_dh_group: "{{ result.ike_v2.ike.dh_group }}"
    esp_encryption: "{{ result.ike_v2.esp.encryption }}"
    esp_integrity: "{{ result.ike_v2.esp.integrity }}"
    esp_dh_group: "{{ result.ike_v2.esp.dh_group }}"
    wait_for_server: true  # Wait for the server to finish updating the connection
  register: result  # Registers the connection as the result

- name: Delete the newly created connection using the 'absent' state
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    state: absent
    name: "{{ result.name }}"
    speed: "{{ result.speed }}"
    high_availability: "{{ result.high_availability }}"
    location_href: "{{ result.location.href }}"
    billing_term: "{{ result.billing_term }}"
    primary_customer_router_ip: "{{ result.primary_customer_router_ip }}"
    secondary_customer_router_ip: "{{ result.secondary_customer_router_ip }}"
    routing_type: "{{ result.routing_type }}"
    customer_asn: "{{ result.customer_asn }}"
    ike_version: "{{ result.ike_version }}"
    ike_encryption: "{{ result.ike_v2.ike.encryption }}"
    ike_integrity: "{{ result.ike_v2.ike.integrity }}"
    ike_dh_group: "{{ result.ike_v2.ike.dh_group }}"
    esp_encryption: "{{ result.ike_v2.esp.encryption }}"
    esp_integrity: "{{ result.ike_v2.esp.integrity }}"
    esp_dh_group: "{{ result.ike_v2.esp.dh_group }}"
    wait_for_server: true  # Wait for the server to finish deleting the connection

- name: Create a ROUTE_BASED_BGP Site IPSec VPN connection with all properties configured
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Site IPSec VPN Connection
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    primary_customer_router_ip: a.b.c.d  # A valid Public IP Address
    secondary_customer_router_ip: a.b.c.d  # A valid Public IP Address
    routing_type: ROUTE_BASED_BGP
    customer_asn: ######
    ike_version: V2
    ike_encryption: AES_128
    ike_integrity: SHA256_HMAC
    ike_dh_group: MODP_2048
    esp_encryption: AES_128
    esp_integrity: SHA256_HMAC
    esp_dh_group: MODP_2048
    # Optional properties start here
    description: My Ansible managed Site IPSec VPN connection
    enable_bgp_password: true # Enable a BGP password for each gateway
    customer_networks:
      - address: a.b.c.d/x  # A valid CIDR address
        name: My AWS accessible CIDR address
    nat_enabled: true
    nat_mappings:
      - a.b.c.d/x  # A valid CIDR address, likely referencing a Customer Network

- name: Create a ROUTE_BASED_STATIC Site IPSec VPN connection with all properties configured
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Site IPSec VPN Connection
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    primary_customer_router_ip: a.b.c.d  # A valid Public IP Address
    secondary_customer_router_ip: a.b.c.d  # A valid Public IP Address
    routing_type: ROUTE_BASED_STATIC
    ike_version: V2
    ike_encryption: AES_128
    ike_integrity: SHA256_HMAC
    ike_dh_group: MODP_2048
    esp_encryption: AES_128
    esp_integrity: SHA256_HMAC
    esp_dh_group: MODP_2048
    customer_networks:  # At least 1 is required
      - address: a.b.c.d/x  # A valid CIDR address
        name: My AWS accessible CIDR address
    # Optional properties start here
    description: My Ansible managed Site IPSec VPN connection
    enable_bgp_password: true
    nat_enabled: true
    nat_mappings:
      - a.b.c.d/x  # A valid CIDR address, likely referencing a Customer Network

- name: Create a POLICY_BASED Site IPSec VPN connection with all properties configured
  aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Site IPSec VPN Connection
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    primary_customer_router_ip: a.b.c.d  # A valid Public IP Address
    secondary_customer_router_ip: a.b.c.d  # A valid Public IP Address
    routing_type: POLICY_BASED
    ike_version: V2
    ike_encryption: AES_128
    ike_integrity: SHA256_HMAC
    ike_dh_group: MODP_2048
    esp_encryption: AES_128
    esp_integrity: SHA256_HMAC
    esp_dh_group: MODP_2048
    traffic_selectors:
      - customer_side: a.b.c.d/x  # A valid CIDR address, likely referencing a Customer Network
        pureport_side: a.b.c.d/x  # A valid CIDR address that points to a different connection's Customer
                                  #    Network or NAT mapped natCidr
    # Optional properties start here
    description: My Ansible managed Site IPSec VPN connection
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
    connection_crud

__IKE_V1_IKE_ENCRYPTION_ALGORITHMS = [
    'AES_128',
    'AES_192',
    'AES_256'
]
__IKE_V1_IKE_INTEGRITY_ALGORITHMS = [
    'MD5_HMAC',
    'SHA1_HMAC',
    'SHA256_HMAC',
    'SHA384_HMAC',
    'SHA512_HMAC'
]
__NO_INTEGRITY_ALGORITHMS = [
    'AES_128_GCM_64',
    'AES_192_GCM_64',
    'AES_256_GCM_64',
    'AES_128_GCM_96',
    'AES_192_GCM_96',
    'AES_256_GCM_96',
    'AES_128_GCM_128',
    'AES_192_GCM_128',
    'AES_256_GCM_128',
    'AES_128_GMAC',
    'AES_192_GMAC',
    'AES_256_GMAC'
]


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

    if 'ikeV1' in connection:
        if connection['ikeV1']['ike']['encryption'] not in __IKE_V1_IKE_ENCRYPTION_ALGORITHMS:
            module.fail_json(msg='For IKE V1, \'ike_encryption\' must '
                                 'be one of %s' % __IKE_V1_IKE_ENCRYPTION_ALGORITHMS)
        if connection['ikeV1']['ike']['integrity'] is None:
            connection['ikeV1']['ike']['integrity'] = 'SHA256_HMAC'
        elif connection['ikeV1']['ike']['integrity'] not in __IKE_V1_IKE_INTEGRITY_ALGORITHMS:
            module.fail_json(msg='For IKE V1, \'ike_integrity\' must '
                                 'be one of %s' % __IKE_V1_IKE_INTEGRITY_ALGORITHMS)
        if connection['ikeV1']['esp']['encryption'] in __NO_INTEGRITY_ALGORITHMS:
            del connection['ikeV1']['esp']['integrity']
    elif 'ikeV2' in connection:
        if connection['ikeV2']['ike']['encryption'] in __NO_INTEGRITY_ALGORITHMS:
            if connection['ikeV2']['ike']['integrity'] is not None:
                del connection['ikeV2']['ike']['integrity']
            if connection['ikeV2']['ike']['prf'] is None:
                connection['ikeV2']['ike']['prf'] = 'SHA_256'
        else:
            if connection['ikeV2']['ike']['integrity'] is None:
                connection['ikeV2']['ike']['integrity'] = 'SHA256_HMAC'
            if connection['ikeV2']['ike']['prf'] is not None:
                del connection['ikeV2']['ike']['prf']

    connection.update(dict(
        type='SITE_IPSEC_VPN',
        authType='PSK',
        location=get_object_link(module, '/locations', 'location_id', 'location_href'),
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
        enableBGPPassword=connection.pop('enableBgpPassword'),
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
            ike_version=dict(
                type='str',
                choices=[
                    'V1',
                    'V2'
                ],
                default='V2'
            ),
            ike_encryption=dict(
                type='str',
                choices=[
                    'NULL',
                    'AES_128',
                    'AES_192',
                    'AES_256',
                    'AES_128_CTR',
                    'AES_192_CTR',
                    'AES_256_CTR',
                    'AES_128_GCM_64',
                    'AES_192_GCM_64',
                    'AES_256_GCM_64',
                    'AES_128_GCM_96',
                    'AES_192_GCM_96',
                    'AES_256_GCM_96',
                    'AES_128_GCM_128',
                    'AES_192_GCM_128',
                    'AES_256_GCM_128'
                ],
                default='AES_128'
            ),
            ike_integrity=dict(
                type='str',
                choices=[
                    'MD5_HMAC',
                    'SHA1_HMAC',
                    'SHA256_HMAC',
                    'SHA384_HMAC',
                    'SHA512_HMAC',
                    'AES_XCBC'
                ]
            ),
            ike_prf=dict(
                type='str',
                choices=[
                    'MD5',
                    'SHA_1',
                    'AES_XCBC',
                    'SHA_256',
                    'SHA_384',
                    'SHA_512'
                ]
            ),
            ike_dh_group=dict(
                type='str',
                choices=[
                    'MODP_1024',
                    'MODP_1536',
                    'MODP_2048',
                    'MODP_3072',
                    'MODP_4096',
                    'MODP_6144',
                    'MODP_8192',
                    'ECP_192',
                    'ECP_224',
                    'ECP_256',
                    'ECP_384',
                    'ECP_521'
                ],
                default='MODP_2048'
            ),
            esp_encryption=dict(
                type='str',
                choices=[
                    'NULL',
                    'AES_128',
                    'AES_192',
                    'AES_256',
                    'AES_128_CTR',
                    'AES_192_CTR',
                    'AES_256_CTR',
                    'AES_128_GCM_64',
                    'AES_192_GCM_64',
                    'AES_256_GCM_64',
                    'AES_128_GCM_96',
                    'AES_192_GCM_96',
                    'AES_256_GCM_96',
                    'AES_128_GCM_128',
                    'AES_192_GCM_128',
                    'AES_256_GCM_128',
                    'AES_128_GMAC',
                    'AES_192_GMAC',
                    'AES_256_GMAC'
                ],
                default='AES_128'
            ),
            esp_integrity=dict(
                type='str',
                choices=[
                    'MD5_HMAC',
                    'SHA1_HMAC',
                    'SHA256_HMAC',
                    'SHA384_HMAC',
                    'SHA512_HMAC',
                    'AES_XCBC'
                ]
            ),
            esp_dh_group=dict(
                type='str',
                choices=[
                    'MODP_1024',
                    'MODP_1536',
                    'MODP_2048',
                    'MODP_3072',
                    'MODP_4096',
                    'MODP_6144',
                    'MODP_8192',
                    'ECP_192',
                    'ECP_224',
                    'ECP_256',
                    'ECP_384',
                    'ECP_521'
                ],
                default='MODP_2048'
            ),
            primary_key=dict(type='str'),
            secondary_key=dict(type='str'),
            traffic_selectors=dict(type='list', default=[], elements='dict'),
            enable_bgp_password=dict(type='bool')
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    mutually_exclusive += [
        ['ike_integrity', 'ike_prf']
    ]
    required_one_of = []
    required_one_of += get_network_mutually_exclusive()
    required_one_of += get_connection_required_one_of()
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
