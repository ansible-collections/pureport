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
    ike_v1_ike_encryption:
        description:
            - The IKE V1 IKE Encryption algorithm
        required: true
        type: str
        choices: ['AES_128', 'AES_192', 'AES_256']
        default: 'AES_128'
    ike_v1_ike_integrity:
        description:
            - The IKE V1 IKE Integrity algorithm
        required: true
        type: str
        choices: ['MD5_HMAC', 'SHA1_HMAC', 'SHA256_HMAC', 'SHA384_HMAC', 'SHA512_HMAC']
        default: 'SHA256_HMAC'
    ike_v1_ike_dh_group:
        description:
            - The IKE V1 Diffie-Hellman group
        required: true
        type: str
        choices: ['MODP_1024', 'MODP_1536', 'MODP_2048', 'MODP_3072', 'MODP_4096', 'MODP_6144',
                  'MODP_8192', 'ECP_192', 'ECP_224', 'ECP_256', 'ECP_384', 'ECP_521']
        default: 'MODP_2048'
    ike_v1_esp_encryption:
        description:
            - The IKE V1 ESP Encryption algorithm
        required: true
        type: str
        choices: ['NULL', 'AES_128', 'AES_192', 'AES_256', 'AES_128_CTR', 'AES_192_CTR', 'AES_256_CTR',
                  'AES_128_GCM_64', 'AES_192_GCM_64', 'AES_256_GCM_64', 'AES_128_GCM_96', 'AES_192_GCM_96',
                  'AES_256_GCM_96', 'AES_128_GCM_128', 'AES_192_GCM_128', 'AES_256_GCM_128', 'AES_128_GMAC',
                  'AES_192_GMAC', 'AES_256_GMAC']
        default: 'AES_128'
    ike_v1_esp_integrity:
        description:
            - The IKE V1 ESP Integrity algorithm
        required: true
        type: str
        choices: ['MD5_HMAC', 'SHA1_HMAC', 'SHA256_HMAC', 'SHA384_HMAC', 'SHA512_HMAC', 'AES_XCBC']
        default: 'SHA256_HMAC'
    ike_v1_esp_dh_group:
        description:
            - The IKE V1 Diffie-Hellman algorithm
        required: true
        type: str
        choices: ['MODP_1024', 'MODP_1536', 'MODP_2048', 'MODP_3072', 'MODP_4096', 'MODP_6144',
                  'MODP_8192', 'ECP_192', 'ECP_224', 'ECP_256', 'ECP_384', 'ECP_521']
        default: 'MODP_2048'
    ike_v2_ike_encryption:
        description:
            - The IKE V2 IKE Encryption algorithm
        required: true
        type: str
        choices: ['NULL', 'AES_128', 'AES_192', 'AES_256', 'AES_128_CTR', 'AES_192_CTR', 'AES_256_CTR',
                  'AES_128_GCM_64', 'AES_192_GCM_64', 'AES_256_GCM_64', 'AES_128_GCM_96', 'AES_192_GCM_96',
                  'AES_256_GCM_96', 'AES_128_GCM_128', 'AES_192_GCM_128', 'AES_256_GCM_128']
        default: 'AES_128'
    ike_v2_ike_integrity:
        description:
            - The IKE V2 IKE Integrity algorithm
        required: true
        type: str
        choices: ['MD5_HMAC', 'SHA1_HMAC', 'SHA256_HMAC', 'SHA384_HMAC', 'SHA512_HMAC', 'AES_XCBC']
        default: 'SHA256_HMAC'
    ike_v2_ike_prf:
        description:
            - The IKE V2 IKE Pseudo-random Function
        required: true
        type: str
        choices: ['MD5', 'SHA_1', 'AES_XCBC', 'SHA_256', 'SHA_384', 'SHA_512']
        default: 'SHA_256'
    ike_v2_ike_dh_group:
        description:
            - The IKE V2 Diffie-Hellman group
        required: true
        type: str
        choices: ['MODP_1024', 'MODP_1536', 'MODP_2048', 'MODP_3072', 'MODP_4096', 'MODP_6144', 'MODP_8192',
                  'ECP_192', 'ECP_224', 'ECP_256', 'ECP_384', 'ECP_521']
        default: 'MODP_2048'
    ike_v2_esp_encryption:
        description:
            - The IKE V2 ESP Encryption algorithm
        required: true
        type: str
        choices: ['NULL', 'AES_128', 'AES_192', 'AES_256', 'AES_128_CTR', 'AES_192_CTR', 'AES_256_CTR',
                  'AES_128_GCM_64', 'AES_192_GCM_64', 'AES_256_GCM_64', 'AES_128_GCM_96', 'AES_192_GCM_96',
                  'AES_256_GCM_96', 'AES_128_GCM_128', 'AES_192_GCM_128', 'AES_256_GCM_128', 'AES_128_GMAC',
                  'AES_192_GMAC', 'AES_256_GMAC']
        default: 'AES_128'
    ike_v2_esp_integrity:
        description:
            - The IKE V2 ESP Integrity algorithm
        required: true
        type: str
        choices: ['MD5_HMAC', 'SHA1_HMAC', 'SHA256_HMAC', 'SHA384_HMAC', 'SHA512_HMAC', 'AES_XCBC']
        default: 'SHA256_HMAC'
    ike_v2_esp_dh_group:
        description:
            - The IKE V2 Diffie-Hellman algorithm
        required: true
        type: str
        choices: ['MODP_1024', 'MODP_1536', 'MODP_2048', 'MODP_3072', 'MODP_4096', 'MODP_6144', 'MODP_8192',
                  'ECP_192', 'ECP_224', 'ECP_256', 'ECP_384', 'ECP_521']
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
    get_network_argument_spec, \
    get_network_mutually_exclusive
from ansible.module_utils.pureport.pureport_crud import get_state_argument_spec
from ansible.module_utils.pureport.pureport_connection_crud import \
    get_wait_for_server_argument_spec, \
    get_connection_argument_spec, \
    connection_crud


__IKE_AEAD_ALGORITHMS = [
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
        'customer_asn',
        'customer_networks',
        'nat',
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
    if connection.get('ike_version') == 'V1':
        connection.update(dict(
            ikeV1=dict(
                ike=dict((k[11:], module.params.get(k)) for k in (
                    'ike_v1_ike_encryption',
                    'ike_v1_ike_integrity',
                    'ike_v1_ike_dh_group'
                )),
                esp=dict((k[11:], module.params.get(k)) for k in (
                    'ike_v1_esp_encryption',
                    'ike_v1_esp_integrity',
                    'ike_v1_esp_dh_group'
                ))
            )
        ))
        if connection['ikeV1']['esp']['encryption'] in __IKE_AEAD_ALGORITHMS:
            connection['ikeV1']['esp'].pop('integrity')
    else:
        connection.update(dict(
            ikeV2=dict(
                ike=dict((k[11:], module.params.get(k)) for k in (
                    'ike_v2_ike_encryption',
                    'ike_v2_ike_integrity',
                    'ike_v2_ike_prf',
                    'ike_v2_ike_dh_group'
                )),
                esp=dict((k[11:], module.params.get(k)) for k in (
                    'ike_v2_esp_encryption',
                    'ike_v2_esp_integrity',
                    'ike_v2_esp_dh_group'
                ))
            )
        ))
        if connection['ikeV2']['ike']['encryption'] in __IKE_AEAD_ALGORITHMS:
            connection['ikeV2']['ike'].pop('integrity')
        else:
            connection['ikeV2']['ike'].pop('prf')

        if connection['ikeV2']['ike']['encryption'] in __IKE_AEAD_ALGORITHMS:
            connection['ikeV2']['ike'].pop('integrity')

    connection.update(dict(
        type="SITE_IPSEC_VPN",
        authType="PSK"
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
    argument_spec.update(get_network_argument_spec())
    argument_spec.update(get_state_argument_spec())
    argument_spec.update(get_wait_for_server_argument_spec())
    argument_spec.update(get_connection_argument_spec())
    argument_spec.update(
        dict(
            primary_customer_router_ip=dict(type="str", required=True),
            secondary_customer_router_ip=dict(type="str"),
            routing_type=dict(
                type="str",
                choices=[
                    'ROUTE_BASED_BGP',
                    'ROUTE_BASED_STATIC',
                    'POLICY_BASED'
                ],
                default='ROUTE_BASED_BGP'
            ),
            physical_address=dict(type="dict"),
            ike_version=dict(type='str', choices=['V1', 'V2'], default='V2'),
            ike_v1_ike_encryption=dict(
                type='str',
                choices=[
                    'AES_128',
                    'AES_192',
                    'AES_256'
                ],
                default='AES_128'
            ),
            ike_v1_ike_integrity=dict(
                type='str',
                choices=[
                    'MD5_HMAC',
                    'SHA1_HMAC',
                    'SHA256_HMAC',
                    'SHA384_HMAC',
                    'SHA512_HMAC'
                ],
                default='SHA256_HMAC'
            ),
            ike_v1_ike_dh_group=dict(
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
            ike_v1_esp_encryption=dict(
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
            ike_v1_esp_integrity=dict(
                type='str',
                choices=[
                    'MD5_HMAC',
                    'SHA1_HMAC',
                    'SHA256_HMAC',
                    'SHA384_HMAC',
                    'SHA512_HMAC',
                    'AES_XCBC'
                ],
                default='SHA256_HMAC'
            ),
            ike_v1_esp_dh_group=dict(
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
            ike_v2_ike_encryption=dict(
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
            ike_v2_ike_integrity=dict(
                type='str',
                choices=[
                    'MD5_HMAC',
                    'SHA1_HMAC',
                    'SHA256_HMAC',
                    'SHA384_HMAC',
                    'SHA512_HMAC',
                    'AES_XCBC'
                ],
                default='SHA256_HMAC'
            ),
            ike_v2_ike_prf=dict(
                type='str',
                choices=[
                    'MD5',
                    'SHA_1',
                    'AES_XCBC',
                    'SHA_256',
                    'SHA_384',
                    'SHA_512'
                ],
                default='SHA_256'
            ),
            ike_v2_ike_dh_group=dict(
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
            ike_v2_esp_encryption=dict(
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
            ike_v2_esp_integrity=dict(
                type='str',
                choices=[
                    'MD5_HMAC',
                    'SHA1_HMAC',
                    'SHA256_HMAC',
                    'SHA384_HMAC',
                    'SHA512_HMAC',
                    'AES_XCBC'
                ],
                default='SHA256_HMAC'
            ),
            ike_v2_esp_dh_group=dict(
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
            traffic_selectors=dict(type='list', default=[]),
            enable_bgp_password=dict(type='bool')
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_network_mutually_exclusive()
    mutually_exclusive += \
        [[ike_v1_field, ike_v2_field]
         for ike_v1_field in [
             'ike_v1_ike_encryption',
             'ike_v1_ike_integrity',
             'ike_v1_ike_dh_group',
             'ike_v1_esp_encryption',
             'ike_v1_esp_integrity',
             'ike_v1_esp_dh_group']
         for ike_v2_field in [
             'ike_v2_ike_encryption',
             'ike_v2_ike_integrity',
             'ike_v2_ike_prf',
             'ike_v2_ike_dh_group',
             'ike_v2_esp_encryption',
             'ike_v2_esp_integrity',
             'ike_v2_esp_dh_group']
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
