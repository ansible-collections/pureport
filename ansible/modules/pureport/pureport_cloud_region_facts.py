#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_cloud_region_facts

short_description: Retrieve a list of cloud regions

version_added: "2.8"

description:
    - "Retrieve a list of cloud regions"

extends_documentation_fragment:
    - pureport_client

author:
    - Matt Traynham (@mtraynham)
'''

EXAMPLES = '''
- name: List cloud regions
  pureport_cloud_region_facts:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
  register: result   # Registers result.cloud_regions

- name: Display all cloud region hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.cloud_regions | json_query('[*].href') }}"
'''

RETURN = '''
cloud_regions:
    description: a list of CloudRegion (dict) objects
    type: list[CloudRegion]
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


def find_cloud_regions(module):
    """
    List cloud regions
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)
    try:
        cloud_regions = client.cloud_regions.list()
        module.exit_json(cloud_regions=cloud_regions)
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
    find_cloud_regions(module)


if __name__ == '__main__':
    main()
