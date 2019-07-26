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
description:
    - "Retrieve a list of cloud regions"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
extends_documentation_fragment:
    - pureport.pureport_ansible_modules.pureport_client
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
    description: A list of CloudRegion (dict) objects.
    returned: success
    type: complex
    contains:
        id:
            description:
                - The cloud region id.
            returned: success
            type: str
            sample: "aws-us-west-1"
        href:
            description:
                - The cloud region href, a path to resource on the server.
            returned: success
            type: str
            sample: "/cloudRegions/aws-us-west-1"
        provider:
            description:
                - The cloud region provider.
            returned: success
            type: str
            sample: "AWS"
        provider_assigned_id:
            description:
                - The cloud region provider's id.
            returned: success
            type: str
            sample: "us-west-1"
        display_name:
            description:
                - A display name for this cloud region.
            returned: success
            type: str
            sample: "US West (N. California)"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from traceback import format_exc

try:
    from pureport.exception.api import ClientHttpException
except ImportError:
    ClientHttpException = None
from ansible_collections.pureport.pureport_ansible_modules.plugins.module_utils.pureport import \
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
        module.exit_json(cloud_regions=[camel_dict_to_snake_dict(cloud_region) for cloud_region in cloud_regions])
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
