#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_account_facts

short_description: Retrieve a list of accounts for the given api credentials

version_added: "2.8"

description:
    - "Retrieve a list of accounts for the given api credentials"

extends_documentation_fragment:
    - pureport_client

author:
    - Matt Traynham (@mtraynham)
'''

EXAMPLES = '''
- name: List accounts for an API key pair
  pureport_networks_facts:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
  register: result   # Registers result.accounts

- name: Display all account hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.accounts | json_query('[*].href') }}"
'''

RETURN = '''
accounts:
    description: a list of Account (dict) objects
    type: list[Account]
'''

from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

try:
    from pureport.exception.api import ClientHttpException
except ImportError:
    ClientHttpException = None
from ansible.module_utils.pureport.pureport import \
    get_client_argument_spec, \
    get_client


def find_accounts(module):
    """
    List accounts
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)
    try:
        accounts = client.accounts.list()
        module.exit_json(accounts=accounts)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    mutually_exclusive = []
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    find_accounts(module)


if __name__ == '__main__':
    main()
