#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_supported_connection_facts
short_description: Retrieve a list of supported connections for an account
description:
    - "Retrieve a list of supported connections for an account"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    account_href:
        required: true
extends_documentation_fragment:
    - pureport_client
    - pureport_account
'''

EXAMPLES = '''
- name: List supported connections for an account
  pureport_supported_connection_facts:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
  register: result   # Registers result.supported_connections

- name: Display all supported connection hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.supported_connections | json_query('[*].href') }}"
'''

RETURN = '''
supported_connections:
    description: A list of SupportedConnection (dict) objects.
    returned: success
    type: complex
    contains:
        id:
            description:
                - The supported connection id.
            returned: success
            type: str
            sample: "us-sea-awsdx-private-50-noha"
        href:
            description:
                - The supported connection href, a path to resource on the server.
            returned: success
            type: str
            sample: "/supportedConnections/us-sea-awsdx-private-50-noha"
        type:
            description:
                - The connection type that is supported.
            returned: success
            type: str
            sample: "AWS_DIRECT_CONNECT"
        location:
            description:
                - The Location Link object of the supported connection.
            returned: success
            type: complex
            contains:
                id:
                    description:
                        - The location id.
                    returned: success
                    type: str
                    sample: "us-sea"
                href:
                    description:
                        - The location href.
                    returned: success
                    type: str
                    sample: "/locations/us-sea"
                title:
                    description:
                        - The location name.
                    returned: success
                    type: str
                    sample: "Seattle, WA"
        reachableCloudRegions:
            description:
                - A list of Cloud Region Link objects supported by the supported connection.
            returned: success
            type: complex
            contains:
                id:
                    description:
                        - The cloud region id.
                    returned: success
                    type: str
                    sample: "aws-us-west-2"
                href:
                    description:
                        - The cloud region href.
                    returned: success
                    type: str
                    sample: "/cloudRegions/aws-us-west-2"
                title:
                    description:
                        - The cloud region name.
                    returned: success
                    type: str
                    sample: "US West (Oregon)"
        groups:
            description:
                - A list of Supported Group Link objects this Supported Connection belongs to.
            returned: success
            type: complex
            contains:
                id:
                    description:
                        - The supported connection group id.
                    returned: success
                    type: str
                    sample: "default"
                href:
                    description:
                        - The supported connection group href.
                    returned: success
                    type: str
                    sample: "/supportedConnections/groups/default"
                title:
                    description:
                        - The supported connection group name.
                    returned: success
                    type: str
                    sample: "Default"
        speed:
            description:
                - The speed of the supported connection.
            returned: success
            type: int
            sample: 50
        highAvailability:
            description:
                - If the connection supports high availability.
            returned: success
            type: bool
            sample: false
        peeringType:
            description:
                - The peering type of the supported connection.
            returned: success
            type: str
            sample: "PRIVATE"
        billingProductId:
            description:
                - The billing product id, a reference to the billing plan for this connection.
            returned: success
            type: str
            sample: "prod_EJ36Dg42H2a9AX"
        billingPlans:
            description:
                - A list of supported billing plans for this supported connection.
            returned: success
            type: complex
            contains:
                id:
                    description:
                        - The billing plan id.
                    returned: success
                    type: str
                    sample: "plan_EJ36MVNfXZ7C3x"
                amount:
                    description:
                        - The amount in cents for this plan.
                    returned: success
                    type: int
                    sample: 15
                term:
                    description:
                        - The frequency at which the 'amount' is accumulated with this connection plan.
                    returned: success
                    type: str
                    sample: "HOURLY"
                billingInterval:
                    description:
                        - The time period billing is accumulated and sent to the user for payment.
                    returned: success
                    type: str
                    sample: "MONTH"
'''

from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

try:
    from pureport.exception.api import ClientHttpException
except ImportError:
    ClientHttpException = None
from ansible.module_utils.pureport.pureport import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_client, \
    get_account_argument_spec, \
    get_account


def find_supported_connections(module):
    """
    List supported connections
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)
    account = get_account(module)
    try:
        supported_connections = client.accounts.supported_connections(account).list()
        module.exit_json(supported_connections=supported_connections)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec(True))
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    find_supported_connections(module)


if __name__ == '__main__':
    main()
