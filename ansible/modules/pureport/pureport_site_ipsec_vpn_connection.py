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
description:
    - "Create, update or delete a Site IPSec VPN connection"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    network_href:
        required: true
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
                        type: double
                    longitude:
                        description:
                            - The logitude
                        required: false
                        type: double
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
            - A list of traffic selectors
        required: false
        type: list
        default: []
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
    - pureport_client
    - pureport_network
    - pureport_state
    - pureport_resolve_existing
    - pureport_wait_for_server
    - pureport_connection_args
'''

EXAMPLES = '''
- name: Create a simple ROUTE_BASED_BGP Site IPSec VPN connection for a network
  pureport_aws_direct_connect_connection:
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
  register: result  # Registers result.connection

- name: Update the newly created connection with changed properties
  pureport_aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: {{ result.connection.name }}
    speed: 100
    high_availability: {{ result.connection.highAvailability }}
    location_href: {{ result.connection.location.href }}
    billing_term: {{ result.connection.billingTerm }}
    primary_customer_router_ip: {{ result.connection.primaryCustomerRouterIP }}
    secondary_customer_router_ip: {{ result.connection.secondaryCustomerRouterIP }}
    routing_type: {{ result.connection.routingType }}
    customer_asn: {{ result.connection.customerASN }}
    ike_version: {{ result.connection.ikeVersion }}
    ike_encryption: {{ result.connection.ikeV2.ike.encryption }}
    ike_integrity: {{ result.connection.ikeV2.ike.integrity }}
    ike_dh_group: {{ result.connection.ikeV2.ike.dhGroup }}
    esp_encryption: {{ result.connection.ikeV2.esp.encryption }}
    esp_integrity: {{ result.connection.ikeV2.esp.integrity }}
    esp_dh_group: {{ result.connection.ikeV2.esp.dhGroup }}
    wait_for_server: true  # Wait for the server to finish updating the connection
  register: result  # Registers result.connection

- name: Delete the newly created connection using the 'absent' state
  pureport_aws_direct_connect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    state: absent
    name: {{ result.connection.name }}
    speed: {{ result.connection.speed }}
    high_availability: {{ result.connection.highAvailability }}
    location_href: {{ result.connection.location.href }}
    billing_term: {{ result.connection.billingTerm }}
    primary_customer_router_ip: {{ result.connection.primaryCustomerRouterIP }}
    secondary_customer_router_ip: {{ result.connection.secondaryCustomerRouterIP }}
    routing_type: {{ result.connection.routingType }}
    customer_asn: {{ result.connection.customerASN }}
    ike_version: {{ result.connection.ikeVersion }}
    ike_encryption: {{ result.connection.ikeV2.ike.encryption }}
    ike_integrity: {{ result.connection.ikeV2.ike.integrity }}
    ike_dh_group: {{ result.connection.ikeV2.ike.dhGroup }}
    esp_encryption: {{ result.connection.ikeV2.esp.encryption }}
    esp_integrity: {{ result.connection.ikeV2.esp.integrity }}
    esp_dh_group: {{ result.connection.ikeV2.esp.dhGroup }}
    wait_for_server: true  # Wait for the server to finish deleting the connection

- name: Create a ROUTE_BASED_BGP Site IPSec VPN connection with all properties configured
  pureport_aws_direct_connect_connection:
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
    routing_type: ROUTE_BASED_BGP
    enable_bgp_password: true # Enable a BGP password for each gateway
    customer_networks:
      - address: a.b.c.d/x  # A valid CIDR address
        name: My AWS accessible CIDR address
    nat_enabled: true
    nat_mappings:
      - a.b.c.d/x  # A valid CIDR address, likely referencing a Customer Network

- name: Create a ROUTE_BASED_STATIC Site IPSec VPN connection with all properties configured
  pureport_aws_direct_connect_connection:
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
  pureport_aws_direct_connect_connection:
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
    type: Connection
'''

from functools import partial
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict

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
    mutually_exclusive += get_client_mutually_exclusive()
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
