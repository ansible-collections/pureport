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
module: ports_info
short_description: Retrieve a list of ports for an account
description:
    - "Retrieve a list of ports for an account"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.account
    - pureport.fabric.account
'''

EXAMPLES = '''
- name: List ports for an account
  ports_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
  register: result   # Registers result.ports

- name: Display all connection hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.connections | json_query('[*].href') }}"
'''

RETURN = '''
ports:
    description: a list of Port (dict) objects
    type: complex
    returned: success
    contains:
        id:
            description:
                - The port id.
            returned: success
            type: str
            sample: "port-rfqj4qc9fO8hDOczEB7Z_Q"
        href:
            description:
                - The port href, a path to resource on the server.
            returned: success
            type: str
            sample: "/ports/port-rfqj4qc9fO8hDOczEB7Z_Q"
        account:
            description:
                - The account this port is tied to.
            returned: success
            type: complex
            contains:
                id:
                    description:
                        - The account id
                    returned: success
                    type: str
                    sample: "ac-XXXXXXXXXXXXXXXXXXXXXX"
                href:
                    description:
                        - The account href
                    returned: success
                    type: str
                    sample: "/accounts/ac-XXXXXXXXXXXXXXXXXXXXXX"
                title:
                    description:
                        - The account title
                    returned: success
                    type: str
                    sample: "My Account"
        facility:
            description:
                - The facility this port is tied to.
            returned: success
            type: complex
            contains:
                id:
                    description:
                        - The facility id
                    returned: success
                    type: str
                    sample: "fac-XXXXXXXXXXXXXXXXXXXXXX"
                href:
                    description:
                        - The facility href
                    returned: success
                    type: str
                    sample: "/facilities/fac-XXXXXXXXXXXXXXXXXXXXXX"
                title:
                    description:
                        - The facility title
                    returned: success
                    type: str
                    sample: "My Facility"
        name:
            description:
                - The name of the port.
            returned: success
            type: str
            sample: "My Port Name"
        description:
            description:
                - The description of the port.
            returned: success
            type: str
            sample: "My port description"
        provider:
            description:
                - The port provider
            returned: success
            type: str
            sample: PACKET_FABRIC
        speed:
            description:
                - The speed of the port.
            returned: success
            type: int
            sample: 1000
        media_type:
            description:
                - The media type of the port.
            returned: success
            type: str
            sample: LX
        availability_domain:
            description:
                - The availability domain of the port.
            returned: success
            type: str
            sample: PRIMARY
        billing_term:
            description:
                - The billing term of the port.
            returned: success
            type: str
            sample: MONTHLY
        state:
            description:
                - The state of the port.
            returned: success
            type: str
            sample: REQUESTED
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
        ports = client.accounts.ports(get_account_id(module)).list()
        module.exit_json(ports=[camel_dict_to_snake_dict(port) for port in ports])
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
