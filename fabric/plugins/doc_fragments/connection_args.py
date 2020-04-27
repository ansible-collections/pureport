# Copyright (c), Pureport, 2020
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    id:
        description:
            - The id of the existing connection.
        required: false
        type: str
    name:
        description:
            - The name of the connection.
        required: true
        type: str
    description:
        description:
            - A description for the connection.
        required: false
        type: str
    speed:
        description:
            - The speed of the connection (Mbps).
        required: true
        type: int
        choices: [50, 100, 200, 300, 400, 500, 1000, 10000]
    high_availability:
        description:
            - If the connection should be high available (2 gateways).
        required: false
        type: bool
    location_id:
        description:
            - The Pureport location id to connect to.
            - This should be the full 'href' path to the Location ReST object (e.g /locations/abc).
            - Only one of 'location_id' or 'location_href' can be supplied for this command.
        required: false
        type: str
    location_href:
        description:
            - The Pureport location to connect to.
            - This should be the full 'href' path to the Location ReST object (e.g /locations/abc).
            - Only one of 'location_id' or 'location_href' can be supplied for this command.
        required: false
        type: str
    billing_term:
        description:
            - The billing term for the connection.
        required: false
        type: str
        choices: ['HOURLY', 'MONTHLY', 'ONE_YEAR', 'TWO_YEAR']
        default: 'HOURLY'
    customer_asn:
        description:
            - A customer Public/Private ASN for the connection.
        required: false
        type: int
    customer_networks:
        description:
            - A list of Connection Customer Networks (e.g dict(address=str, name=str)).
        required: false
        type: list
        default: []
        elements: dict
        suboptions:
            address:
                description:
                    - A CIDR (a.b.c.d/n) address representing a subnet behind this connection.
                required: true
                type: str
            name:
                description:
                    - A name to give this subnet CIDR.
    nat_enabled:
        description:
            - If NAT should be enabled
        type: bool
        default: false
    nat_mappings:
        description:
            - A list of CIDR's (a.b.c.d/n) addresses that should be mapped with NAT.
            - This should likely reference the customer_networks supplied on the connection.
        required: false
        type: list
        elements: str
    tags:
        description:
            - A map of tags to use for the connection.
            - This should be a mapping of string to string pairs with no duplicate keys.
        required: false
        type: dict
    '''
