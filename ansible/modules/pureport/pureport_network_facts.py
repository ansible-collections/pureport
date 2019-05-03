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

version_added: "2.8"

description:
    - "Retrieve a list of networks for an account"

options:
    account_href:
        required: true

extends_documentation_fragment:
    - pureport_client
    - pureport_account

author:
    - Matt Traynham (@mtraynham)
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
    description: a list of Network (dict) objects
    type: list[Network]
'''

from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

try:
    from pureport.exception.api import ClientHttpException
except ImportError:
    ClientHttpException = None
from ansible.module_utils.pureport.pureport import \
    get_client_argument_spec, \
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
        module.exit_json(networks=networks)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec(True))
    mutually_exclusive = []
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    find_networks(module)


if __name__ == '__main__':
    main()
