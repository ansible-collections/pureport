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
module: access_token_info
short_description: Retrieve an access token to use with the Pureport API
description:
    - "Retrieve an access token to use with the Pureport API"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    api_base_url:
        description:
            - The host url for the Pureport API.
        required: false
        type: str
    api_key:
        description:
            - The pre-configured API Key for a Pureport Account.
        required: true
        type: str
    api_secret:
        description:
            - The pre-configured API Secret for a Pureport Account.
        required: true
        type: str
'''

EXAMPLES = '''
- name: Retrieve the access token for an api key and secret
  access_token_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
  register: result   # Registers result.access_token

- name: Set the access token as a fact
  set_fact:
    access_token: result.access_token
'''

RETURN = '''
access_token:
    description:
        - An access token that can be used with other Pureport facts.
    returned: success
    type: str
'''

from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

try:
    from pureport.api.client import Client
    from pureport.exception.api import ClientHttpException
    HAS_PUREPORT_CLIENT = True
except ImportError:
    HAS_PUREPORT_CLIENT = False
    Client = None
    ClientHttpException = None


def main():
    argument_spec = dict(
        api_base_url=dict(type='str'),
        api_key=dict(type='str', required=True),
        api_secret=dict(type='str', required=True, no_log=True)
    )
    mutually_exclusive = []
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    if not HAS_PUREPORT_CLIENT:
        module.fail_json(msg='pureport-client required for this module')
    client = Client(module.params.get('api_base_url'))
    try:
        module.exit_json(access_token=client.login(module.params.get('api_key'), module.params.get('api_secret')))
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
