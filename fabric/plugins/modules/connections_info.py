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
module: connections_info
short_description: Retrieve a list of connections for a account or network
description:
    - "Retrieve a list of connections for a account or network"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    account_id:
        description:
            - The Pureport Account object's id field.
            - Only one of 'account_id', 'account_href', 'network_id' or 'network_href' should be supplied for this command.
    account_href:
        description:
            - The Pureport Account object's href field.
            - This should be the full 'href' path to the Account ReST object (e.g /accounts/abc).
            - Only one of 'account_id', 'account_href', 'network_id' or 'network_href' should be supplied for this command.
    network_id:
        description:
            - The Pureport Network object's id field.
            - Only one of 'account_id', 'account_href', 'network_id' or 'network_href' should be supplied for this command.
    network_href:
        description:
            - The Pureport Network object's href field.
            - This should be the full 'href' path to the Network ReST object (e.g /networks/abc).
            - Only one of 'account_id', 'account_href', 'network_id' or 'network_href' should be supplied for this command.
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.account
    - pureport.fabric.network
'''

EXAMPLES = '''
- name: List connections for an account
  connections_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
  register: result   # Registers result.connections

- name: List connections for a network
  connections_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
  register: result   # Registers result.connections

- name: Display all connection hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.connections | json_query('[*].href') }}"
'''

RETURN = '''
connections:
    description: a list of Connection (dict) objects
    type: list
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from itertools import chain
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
    get_account_id, \
    get_network_argument_spec, \
    get_network_mutually_exclusive, \
    get_network_id


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec())
    argument_spec.update(get_network_argument_spec())
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    required_one_of = []
    required_one_of += [
        list(chain.from_iterable(get_account_mutually_exclusive() + get_network_mutually_exclusive()))
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True
    )
    try:
        connections = None
        account_id = get_account_id(module)
        network_id = get_network_id(module)
        client = get_client(module)
        # Retrieve connections from the account
        if account_id is not None:
            connections = client.accounts.connections(account_id).list()
        # Retrieve connections from the network
        elif network_id is not None:
            connections = client.networks.connections(network_id).list()
        module.exit_json(connections=[camel_dict_to_snake_dict(connection) for connection in connections])
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
