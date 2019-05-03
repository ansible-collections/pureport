class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    id:
        description:
            - The id of the connection (required if updating/deleting).
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
    location_href:
        description:
            - The Pureport location to connect to.
            - This should be the full 'href' path to the Location ReST object (e.g /locations/abc).
        required: true
        type: dict
    billing_term:
        description:
            - The billing term for the connection.
        required: true
        type: str
        choices: ['HOURLY']
    customer_asn:
        description:
            - A customer Public/Private ASN for the connection.
        required: false
        type: long
    customer_networks:
        description:
            - A list of Connection Customer Networks (e.g dict(address=str, name=str)).
        required: false
        type: list
        default: []
    nat_enabled:
        description:
            - If NAT should be enabled
        type: bool
        default: false
    nat_mappings:
        description:
            - A list of CIDR's that should be mapped with NAT
        required: false
        type: list
    '''
