#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_location_facts

short_description: Retrieve a list of locations

version_added: "2.8"

description:
    - "Retrieve a list of locations"

extends_documentation_fragment:
    - pureport_client

author:
    - Matt Traynham (@mtraynham)
'''

EXAMPLES = '''
- name: List locations
  pureport_location_facts:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
  register: result   # Registers result.locations

- name: Display all locations hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.locations | json_query('[*].href') }}"
'''

RETURN = '''
locations:
    description: a list of Location (dict) objects
    type: list[Location]
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


def find_locations(module):
    """
    List locations
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)
    try:
        locations = client.locations.list()
        module.exit_json(locations=locations)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    find_locations(module)


if __name__ == '__main__':
    main()
