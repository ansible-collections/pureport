#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_facility_facts
short_description: Retrieve a list of facilities
description:
    - "Retrieve a list of facilities"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
extends_documentation_fragment:
    - pureport.pureport.pureport_client
'''

EXAMPLES = '''
- name: List facilities
  pureport_facility_facts:
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
                    required: false
                    type: str
                city:
                    description:
                        - The city
                    required: false
                    type: str
                state:
                    description:
                        - The state
                    required: false
                    type: str
                postal_code:
                    description:
                        - The postal code
                    required: false
                    type: str
                country:
                    description:
                        - The country
                    required: false
                    type: str
                geo_coordinates:
                    description:
                        - A dict representing the geo coordinates of a facility
                    required: false
                    type: complex
                    contains:
                        latitude:
                            description:
                                - The latitude
                            required: false
                            type: double
                        longitude:
                            description:
                                - The longitude
                            required: false
                            type: double
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from traceback import format_exc

try:
    from pureport.exception.api import ClientHttpException
except ImportError:
    ClientHttpException = None
from ansible_collections.pureport.pureport.plugins.module_utils.pureport import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_client


def __format_facility(facility):
    """
    Format a facility for output
    :param Facility facility: the facility
    :rtype: Facility
    """
    formatted_facility = dict(facility)
    alt_ids = formatted_facility.pop('altIds')
    formatted_facility = camel_dict_to_snake_dict(facility)
    formatted_facility.update(dict(alt_ids=alt_ids))
    return formatted_facility


def find_facilities(module):
    """
    List facilities
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)
    try:
        facilities = client.facilities.list()

        module.exit_json(facilities=[__format_facility(facility) for facility in facilities])
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
    find_facilities(module)


if __name__ == '__main__':
    main()
