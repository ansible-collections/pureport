#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_connection_facts

short_description: Retrieve a list of connections for a account or network

version_added: "2.8"

description:
    - "Retrieve a list of connections for a account or network"

options:
    account_href:
        description:
            - The Pureport Account object.
            - This should be the full 'href' path to the Account ReST object (e.g /accounts/abc).
            - One of 'account_href' or 'network_href' should be supplied for this command, but not both.
    network_href:
        description:
            - The Pureport Network object.
            - This should be the full 'href' path to the Network ReST object (e.g /networks/abc).
            - One of 'account_href' or 'network_href' should be supplied for this command, but not both.

extends_documentation_fragment:
    - pureport_client
    - pureport_account
    - pureport_network

author:
    - Matt Traynham (@mtraynham)
'''

EXAMPLES = '''
- name: List connections for an account
  pureport_networks_facts:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
  register: result   # Registers result.connections

- name: List connections for a network
  pureport_networks_facts:
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
    type: list[Connection]
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
    get_account, \
    get_network_argument_spec, \
    get_network


def find_connections(module):
    """
    List connections
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)

    connections = None
    # Retrieve connections from the account
    if module.params.get('account_href') is not None:
        account = get_account(module)
        try:
            connections = client.accounts.connections(account).list()
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())
    # Retrieve connections from the network
    elif module.params.get('network_href') is not None:
        network = get_network(module)
        try:
            connections = client.networks.connections(network).list()
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())
    else:
        module.fail_json(msg='One of account_href or network_href '
                             'arguments should be provided.')

    module.exit_json(connections=connections)


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec())
    argument_spec.update(get_network_argument_spec())
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    mutually_exclusive += [
        ['account_href', 'network_href']
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    find_connections(module)


if __name__ == '__main__':
    main()
