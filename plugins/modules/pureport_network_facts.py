#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_network_facts
short_description: Retrieve a list of networks for an account
description:
    - "Retrieve a list of networks for an account"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    account_href:
        required: true
extends_documentation_fragment:
    - pureport.pureport_ansible_modules.pureport_client
    - pureport.pureport_ansible_modules.pureport_account
'''

EXAMPLES = '''
- name: List networks for an account
  pureport_networks_facts:
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
from ansible_collections.pureport.pureport_ansible_modules.plugins.module_utils.pureport import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_client, \
    get_account_argument_spec, \
    get_account


def find_networks(module):
    """
    List networks
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)
    account = get_account(module)
    try:
        networks = client.accounts.networks(account).list()
        module.exit_json(networks=[camel_dict_to_snake_dict(network) for network in networks])
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
    find_networks(module)


if __name__ == '__main__':
    main()
