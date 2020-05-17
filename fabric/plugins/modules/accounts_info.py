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
module: accounts_info
short_description: Retrieve a list of accounts for the given api credentials
description:
    - "Retrieve a list of accounts for the given api credentials"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
extends_documentation_fragment:
    - pureport.fabric.client
'''

EXAMPLES = '''
- name: List accounts for an API key pair
  accounts_info:
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
    description: A list of Account (dict) objects.
    returned: success
    type: complex
    contains:
        id:
            description:
                - The account id
            returned: success
            type: str
            sample: "ac-1kAtS97scnsIkdB291YCbg"
        href:
            description:
                - The account href, a path to resource on the server.
            returned: success
            type: str
            sample: "/accounts/ac-1kAtS97scnsIkdB291YCbg"
        name:
            description:
                - The account name.
            returned: success
            type: str
            sample: "My Account Name"
        description:
            description:
                - The account description.
            returned: success
            type: str
            sample: "My account description"
        parent:
            description:
                - The parent Account Link object.
            returned: success
            type: complex
            contains:
                id:
                    description:
                        - The parent account id.
                    returned: success
                    type: str
                    sample: "ac-K0TL4YjBctBOHyVKj9hHaQ"
                href:
                    description:
                        - The parent account href.
                    returned: success
                    type: str
                    sample: "/accounts/ac-K0TL4YjBctBOHyVKj9hHaQ"
                title:
                    description:
                        - The parent account name.
                    returned: success
                    type: str
                    sample: "My Parent Account Name"
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
    get_client


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True
    )
    try:
        client = get_client(module)
        accounts = client.accounts.list()
        module.exit_json(accounts=[camel_dict_to_snake_dict(account) for account in accounts])
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
