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
module: networks_info
short_description: Retrieve a list of networks for an account
description:
    - "Retrieve a list of networks for an account"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.account
'''

EXAMPLES = '''
- name: List networks for an account
  networks_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
  register: result   # Registers result.networks

- name: Display all network hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.networks | json_query('[*].href') }}"
'''

RETURN = '''
networks:
    description: A list of Network (dict) objects.
    returned: success
    type: complex
    contains:
        id:
            description:
                - The network id.
            returned: success
            type: str
            sample: "network-rfqj4qc9fO8hDOczEB7Z_Q"
        href:
            description:
                - The network href, a path to resource on the server.
            returned: success
            type: str
            sample: "/networks/network-rfqj4qc9fO8hDOczEB7Z_Q"
        name:
            description:
                - The name of the network.
            returned: success
            type: str
            sample: "My Network Name"
        description:
            description:
                - The description of the network.
            returned: success
            type: str
            sample: "My network description"
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
        networks = client.accounts.networks(get_account_id(module)).list()
        module.exit_json(networks=[camel_dict_to_snake_dict(network) for network in networks])
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
