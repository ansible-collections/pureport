#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_option_facts

short_description: Retrieve a list of option enumerations used for creating connections

version_added: "2.8"

description:
    - "Retrieve a list of option enumerations used for creating connections"

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

extends_documentation_fragment:
    - pureport_client

author:
    - Matt Traynham (@mtraynham)
'''

EXAMPLES = '''
- name: List options
  pureport_location_facts:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
  register: result   # Registers result.options

- name: List a subset of options
  pureport_location_facts:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    types:
      - IKEV2IKEPRF
  register: result   # Registers result.options
'''

RETURN = '''
options:
    description: a list of Option (dict) objects
    type: list[Option]
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
    get_client


def find_options(module):
    """
    List options
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)
    try:
        options = client.options.list(*module.params.get('types'))
        module.exit_json(options=options)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


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
            ]
        )
    ))
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    find_options(module)


if __name__ == '__main__':
    main()
