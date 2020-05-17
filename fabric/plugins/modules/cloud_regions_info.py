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
module: cloud_regions_info
short_description: Retrieve a list of cloud regions
description:
    - "Retrieve a list of cloud regions"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
extends_documentation_fragment:
    - pureport.fabric.client
'''

EXAMPLES = '''
- name: List cloud regions
  cloud_regions_info:
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
        cloud_regions = client.cloud_regions.list()
        module.exit_json(cloud_regions=[camel_dict_to_snake_dict(cloud_region) for cloud_region in cloud_regions])
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
