#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_cloud_service_facts

short_description: Retrieve a list of cloud services

version_added: "2.8"

description:
    - "Retrieve a list of cloud services"

extends_documentation_fragment:
    - pureport_client

author:
    - Matt Traynham (@mtraynham)
'''

EXAMPLES = '''
- name: List cloud services
  pureport_cloud_service_facts:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
  register: result   # Registers result.cloudServices

- name: Display all cloud service hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.cloudServices | json_query('[*].href') }}"
'''

RETURN = '''
cloud_services:
    description: a list of CloudService (dict) objects
    type: list[CloudService]
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


def find_cloud_services(module):
    """
    List cloud services
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)
    try:
        cloud_services = client.cloud_services.list()
        module.exit_json(cloud_services=cloud_services)
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
    find_cloud_services(module)


if __name__ == '__main__':
    main()
