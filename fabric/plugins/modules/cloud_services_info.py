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
module: cloud_services_info
short_description: Retrieve a list of cloud services
description:
    - "Retrieve a list of cloud services"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
extends_documentation_fragment:
    - pureport.fabric.client
'''

EXAMPLES = '''
- name: List cloud services
  cloud_services_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
  register: result   # Registers result.cloud_services

- name: Display all cloud service hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.cloud_services | json_query('[*].href') }}"
'''

RETURN = '''
cloud_services:
    description: A list of CloudService (dict) objects.
    returned: success
    type: complex
    contains:
        id:
            description:
                - The cloud service id.
            returned: success
            type: str
            sample: "aws-s3-us-west-1"
        href:
            description:
                - The cloud service href, a path to resource on the server.
            returned: success
            type: str
            sample: "/cloudServices/aws-s3-us-west-1"
        provider:
            description:
                - The cloud service provider.
            returned: success
            type: str
            sample: "AWS"
        name:
            description:
                - A name for this cloud service.
            returned: success
            type: str
            sample: "AWS S3 us-west-1"
        service:
            description:
                - The service name for the provider.
            returned: success
            type: str
            sample: "S3"
        ipv4_prefix_count:
            description:
                - The number of ipv4 prefixes this service uses.
            returned: success
            type: int
            sample: 3
        ipv6_prefix_count:
            description:
                - The number of ipv6 prefixes this service uses.
            returned: success
            type: int
            sample: 4
        cloud_region:
            description:
                - The Cloud Region Link object which this service corresponds to.
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
                        - The cloud region href.
                    returned: success
                    type: str
                    sample: "/cloudRegions/aws-us-west-1"
                title:
                    description:
                        - The cloud region display name.
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
        cloud_services = client.cloud_services.list()
        module.exit_json(cloud_services=[camel_dict_to_snake_dict(cloud_service) for cloud_service in cloud_services])
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
