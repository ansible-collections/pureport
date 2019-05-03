#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_connection_facts

short_description: Retrieve a list of Connections

version_added: "2.8"

description:
    - "Retrieve a list of Connections"

extends_documentation_fragment:
    - pureport_client
    - pureport_account
    - pureport_network

author:
    - Matt Traynham (@mtraynham)
'''

EXAMPLES = '''
- name: List connections for an account
  pureport_connection_facts:
    api_key: abc
    api_secret: xyz
    account_id: 123

- name: List connection for a network
  pureport_connection_facts:
    api_key: abc
    api_secret: xyz
    network_id: 123

### List connections for a network and display their names using json query filter
### https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#json-query-filter
- name: List connections for a network
  pureport_connection_facts:
    api_key: abc
    api_secret: xyz
    network_id: 123
  register: result

- name: Display all connection ids
  debug:
    var: item
  loop: "{{ result.connections | json_query('[*].id') }}"
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
    pass
from ansible.module_utils.pureport.pureport import \
    get_client_argument_spec, \
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
