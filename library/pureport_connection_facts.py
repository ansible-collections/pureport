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

version_added: "2.7"

description:
    - "Retrieve a list of Connections"

options:
    api_base_url:
        description:
            - The host url for the Pureport API
        required: false
        type: str
    api_key:
        description:
            - This is the pre-configured API Key for a Pureport Account
        required: true
        type: str
    api_secret:
        description:
            - This is the pre-configured API Secret for a Pureport Account
        required: true
        type: str
    account:
        description:
            - The account to retrieve connections for
        required: false
        type: dict
    account_id:
        description:
            - The account id to retrieve connections for
        required: false
        type: str
    network:
        description:
            - The network to retrieve connections for
        required: false
        type: dict
    network_id:
        description:
            - The network id to retrieve connections for
        required: false
        type: str

extends_documentation_fragment:
    - pureport

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
from module_utils.pureport import \
    get_client_argument_spec, \
    get_client, \
    get_account_argument_spec, \
    get_account_mutually_exclusive, \
    get_account, \
    get_network_argument_spec, \
    get_network_mutually_exclusive, \
    get_network


def find_connections(module):
    """
    List connections
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)

    connections = None
    # Retrieve connections from the account
    if module.params.get('account') is not None or \
            module.params.get('account_id') is not None:
        account = get_account(module, client)
        try:
            connections = client.accounts.connections(account).list()
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())
    # Retrieve connections from the network
    elif module.params.get('network') is not None or \
            module.params.get('network_id') is not None:
        network = get_network(module, client)
        try:
            connections = client.networks.connections(network).list()
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())
    else:
        module.fail_json(msg='One of account, account_id, network, '
                             'or network_id arguments should be provided.')

    module.exit_json(connections=connections)


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec())
    argument_spec.update(get_network_argument_spec())
    mutually_exclusive = []
    mutually_exclusive += [
        get_account_mutually_exclusive()[0] + get_network_mutually_exclusive()[0]
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    find_connections(module)


if __name__ == '__main__':
    main()
