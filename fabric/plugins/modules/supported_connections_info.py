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
module: supported_connections_info
short_description: Retrieve a list of supported connections for an account
description:
    - "Retrieve a list of supported connections for an account"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.account
'''

EXAMPLES = '''
- name: List supported connections for an account
  supported_connections_info:
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
        reachable_cloud_Regions:
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
        high_availability:
            description:
                - If the connection supports high availability.
            returned: success
            type: bool
            sample: false
        peering_type:
            description:
                - The peering type of the supported connection.
            returned: success
            type: str
            sample: "PRIVATE"
        billing_product_id:
            description:
                - The billing product id, a reference to the billing plan for this connection.
            returned: success
            type: str
            sample: "prod_EJ36Dg42H2a9AX"
        billing_plans:
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
                billing_interval:
                    description:
                        - The time period billing is accumulated and sent to the user for payment.
                    returned: success
                    type: str
                    sample: "MONTH"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from traceback import format_exc

try:
    from pureport.exception.api import ClientHttpException
except ImportError:
    ClientHttpException = None
from ..module_utils.pureport_client import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_client, \
    get_account_argument_spec, \
    get_account_mutually_exclusive, \
    get_account_id


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec())
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    required_one_of = []
    required_one_of += get_account_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        required_one_of=required_one_of,
        supports_check_mode=True
    )
    try:
        client = get_client(module)
        supported_connections = client.accounts.supported_connections(get_account_id(module)).list()
        module.exit_json(supported_connections=[camel_dict_to_snake_dict(supported_connection)
                                                for supported_connection in supported_connections])
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
