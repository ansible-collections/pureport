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
module: facilities_info
short_description: Retrieve a list of facilities
description:
    - "Retrieve a list of facilities"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
extends_documentation_fragment:
    - pureport.fabric.client
'''

EXAMPLES = '''
- name: List facilities
  facilities_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
  register: result   # Registers result.facilities

- name: Display all facility hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.facilities | json_query('[*].href') }}"
'''

RETURN = '''
facilities:
    description: A list of Facility (dict) objects.
    returned: success
    type: complex
    contains:
        id:
            description:
                - The facility id.
            returned: success
            type: str
            sample: "us-colo-atl"
        href:
            description:
                - The facility href, a path to resource on the server.
            returned: success
            type: str
            sample: "/facilities/us-colo-atl"
        name:
            description:
                - The facility name.
            returned: success
            type: str
            sample: "Colo Atl"
        vendor:
            description:
                - The facility vendor
            returned: success
            type: str
            sample: "JTC"
        state:
            description:
                - The state of the facility
            returned: success
            type: str
            sample: "ACTIVE"
        physical_address:
            description:
                - Information about the physical address of the facility.
            returned: success
            type: complex
            contains:
                street:
                    description:
                        - The street address
                    returned: success
                    type: str
                city:
                    description:
                        - The city
                    returned: success
                    type: str
                state:
                    description:
                        - The state
                    returned: success
                    type: str
                postal_code:
                    description:
                        - The postal code
                    returned: success
                    type: str
                country:
                    description:
                        - The country
                    returned: success
                    type: str
                geo_coordinates:
                    description:
                        - A dict representing the geo coordinates of a facility
                    returned: success
                    type: complex
                    contains:
                        latitude:
                            description:
                                - The latitude
                            returned: success
                            type: float
                        longitude:
                            description:
                                - The longitude
                            returned: success
                            type: float
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


def __format_facility(facility):
    """
    Format a facility for output
    :param dict facility: the facility
    :rtype: pureport.api.client.Facility
    """
    formatted_facility = dict(facility)
    alt_ids = formatted_facility.pop('altIds')
    formatted_facility = camel_dict_to_snake_dict(facility)
    formatted_facility.update(dict(alt_ids=alt_ids))
    return formatted_facility


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
        facilities = client.facilities.list()
        module.exit_json(facilities=[__format_facility(facility) for facility in facilities])
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
