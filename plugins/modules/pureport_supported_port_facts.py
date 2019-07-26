#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_supported_port_facts
short_description: Retrieve a list of supported ports for an account
description:
    - "Retrieve a list of supported ports for an account"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    account_href:
        required: true
    facility_href:
        description:
            - The Pureport Facility object.
            - This should be the full 'href' path to the Facility ReST object (e.g /facilities/abc).
        required: true
        type: str
extends_documentation_fragment:
    - pureport.pureport_ansible_modules.pureport_client
    - pureport.pureport_ansible_modules.pureport_account
'''

EXAMPLES = '''
- name: List supported ports
  pureport_supported_port_facts:
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
from ansible_collections.pureport.pureport_ansible_modules.plugins.module_utils.pureport import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_client, \
    get_account_argument_spec, \
    get_account


def find_supported_ports(module):
    """
    List supported ports
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)
    account = get_account(module)
    try:
        supported_ports = client.accounts \
            .supported_ports(account) \
            .list({'id': module.params.get('facility_href').split('/')[-1]})
        module.exit_json(supported_ports=[camel_dict_to_snake_dict(supported_port)
                                          for supported_port in supported_ports])
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec(True))
    argument_spec.update(dict(
        facility_href=dict(type='str', required=True)
    ))
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    find_supported_ports(module)


if __name__ == '__main__':
    main()
