#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_supported_connection_facts

short_description: Retrieve a list of supported connections for an account

version_added: "2.8"

description:
    - "Retrieve a list of supported connections for an account"

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
- name: List supported connections for an account
  pureport_supported_connection_facts:
    api_access_token: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
  register: result   # Registers result.supported_connections

- name: Display all supported connection hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.supported_connections | json_query('[*].href') }}"
'''

RETURN = '''
supported_connections:
    description: a list of SupportedConnection (dict) objects
    type: list[SupportedConnection]
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


def find_supported_connections(module):
    """
    List supported connections
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)
    account = get_account(module)
    try:
        supported_connections = client.accounts.supported_connections(account).list()
        module.exit_json(supported_connections=supported_connections)
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
    find_supported_connections(module)


if __name__ == '__main__':
    main()
