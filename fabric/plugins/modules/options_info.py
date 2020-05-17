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
module: options_info
short_description: Retrieve a list of option enumerations used for creating connections
description:
    - "Retrieve a list of option enumerations used for creating connections"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    types:
        description:
            - a list of types to filter the results
        type: list
        choices: ['IKEV1IKEEncryption', 'IKEV1IKEIntegrity', 'IKEV1IKEDHGroup', 'IKEV1ESPEncryption',
                  'IKEV1ESPIntegrity', 'IKEV1ESPDHGroup', 'IKEV2IKEEncryption', 'IKEV2IKEPRF',
                  'IKEV2IKEIntegrity', 'IKEV2IKEDHGroup', 'IKEV2ESPEncryption', 'IKEV2ESPIntegrity',
                  'IKEV2ESPDHGroup']
        default: []
        elements: str
extends_documentation_fragment:
    - pureport.fabric.client
'''

EXAMPLES = '''
- name: List options
  options_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
  register: result   # Registers result.options

- name: List a subset of options
  options_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    types:
      - IKEV2IKEPRF
  register: result   # Registers result.options
'''

RETURN = '''
options:
    description: a dict of Option type keys to their list of available Option values (dict) objects.
    returned: success
    type: complex
    contains:
        key:
            description:
                - The option group type.
            returned: success
            type: str
            sample: "IKEV1IKEEncryption"
        value:
            description:
                - The option group available values.
            returned: success
            type: complex
            contains:
                value:
                    description:
                        - The option's value.
                    returned: success
                    type: str
                    sample: "AES_128"
                description:
                    description:
                        - The option's description.
                    returned: success
                    type: str
                    sample: "128 bit AES-CBC"
                aead:
                    description:
                        - If the option is considered authenticated encryption with associated data (AEAD).
                    returned: success
                    type: bool
                    sample: false
                unsafe:
                    description:
                        - If the option is deemed unsafe because of encryption standards.
                    returned: success
                    type: bool
                    sample: false
                default:
                    description:
                        - If the option is considered the default option for this group type.
                    returned: success
                    type: bool
                    sample: true
'''

from ansible.module_utils.basic import AnsibleModule
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
    argument_spec.update(dict(
        types=dict(
            type="list",
            default=[],
            choices=[
                'IKEV1IKEEncryption',
                'IKEV1IKEIntegrity',
                'IKEV1IKEDHGroup',
                'IKEV1ESPEncryption',
                'IKEV1ESPIntegrity',
                'IKEV1ESPDHGroup',
                'IKEV2IKEEncryption',
                'IKEV2IKEPRF',
                'IKEV2IKEIntegrity',
                'IKEV2IKEDHGroup',
                'IKEV2ESPEncryption',
                'IKEV2ESPIntegrity',
                'IKEV2ESPDHGroup'
            ],
            elements='str'
        )
    ))
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True
    )
    try:
        client = get_client(module)
        options = client.options.list(module.params.get('types'))
        module.exit_json(options=options)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
