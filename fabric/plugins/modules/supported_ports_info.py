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
module: supported_ports_info
short_description: Retrieve a list of supported ports for an account
description:
    - "Retrieve a list of supported ports for an account"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    facility_id:
        description:
            - The Pureport Facility id.
            - Only one of 'facility_id' or 'facility_href' can be supplied for this command.
        required: false
        type: str
    facility_href:
        description:
            - The Pureport Facility href.
            - This should be the full 'href' path to the Facility ReST object (e.g /facilities/abc).
            - Only one of 'facility_id' or 'facility_href' can be supplied for this command.
        required: false
        type: str
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.account
'''

EXAMPLES = '''
- name: List supported ports
  supported_ports_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
    facility_href: /facilities/us-colo-atl
  register: result   # Registers result.supported_ports
'''

RETURN = '''
supported_ports:
    description: A list of SupportedPort (dict) objects.
    returned: success
    type: complex
    contains:
        provider:
            description:
                - The supported port provider.
            returned: success
            type: str
            sample: "PACKET_FABRIC"
        facility:
            description:
                - The Facility Link object of the supported port.
            returned: success
            type: complex
            contains:
                id:
                    description:
                        - The facility id.
                    returned: success
                    type: str
                    sample: "us-colo-atl"
                href:
                    description:
                        - The facility href.
                    returned: success
                    type: str
                    sample: "/facilities/us-colo-atl"
                title:
                    description:
                        - The facility name.
                    returned: success
                    type: str
                    sample: "Colo ATL"
        speed:
            description:
                - The speed of the supported port.
            returned: success
            type: int
            sample: 1000
        media_types:
            description:
                - The list of available media types for the specified port.
            returned: success
            type: list
            elements: str
            sample: ["LX", "LR4"]
        availability_domains:
            description:
                - The list of availability domains for the specified port.
            returned: success
            type: str
            sample: ["PRIMARY", "SECONDARY"]
        billing_plans:
            description:
                - A list of supported billing plans for this supported port.
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
                setup_amount:
                    description:
                        - The amount in cents for this initial setup fee
                    returned: success
                    type: int
                    sample: 1809
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
    get_object_id, \
    get_account_argument_spec, \
    get_account_mutually_exclusive, \
    get_account_id


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec())
    argument_spec.update(dict(
        facility_id=dict(type='str'),
        facility_href=dict(type='str')
    ))
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    required_one_of = []
    required_one_of += get_account_mutually_exclusive()
    required_one_of += [
        ['facility_id', 'facility_href']
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        required_one_of=required_one_of,
        supports_check_mode=True
    )
    try:
        client = get_client(module)
        supported_ports = client.accounts \
            .supported_ports(get_account_id(module)) \
            .list(get_object_id(module, 'facility_id', 'facility_href'))
        module.exit_json(supported_ports=[camel_dict_to_snake_dict(supported_port)
                                          for supported_port in supported_ports])
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
