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
description:
    - "Retrieve a list of locations"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
extends_documentation_fragment:
    - pureport_client
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
    description: A list of Location (dict) objects.
    returned: success
    type: complex
    contains:
        id:
            description:
                - The location id.
            returned: success
            type: str
            sample: "us-sea"
        href:
            description:
                - The location href, a path to resource on the server.
            returned: success
            type: str
            sample: "/locations/us-sea"
        name:
            description:
                - The location name.
            returned: success
            type: str
            sample: "Seattle, WA"
        geo_coordinates:
            description:
                - The location's geo-coordinates.
            returned: success
            type: complex
            contains:
                latitude:
                    description:
                        - The location's latitude.
                    returned: success
                    type: double
                    sample: 47.6062
                longitude:
                    description:
                        - The location's longitude.
                    returned: success
                    type: double
                    sample: -122.3321
        location_links:
            description:
                - A list of other Location Link objects that this Location has a Pureport backbone connection to.
            returned: success
            type: complex
            contains:
                id:
                    description:
                        - The other location id.
                    returned: success
                    type: str
                    sample: "us-ral"
                href:
                    description:
                        - The other location href.
                    returned: success
                    type: str
                    sample: "/locations/us-ral"
                title:
                    description:
                        - The other location name.
                    returned: success
                    type: str
                    sample: "Raleigh, NC"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
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
        module.exit_json(locations=[camel_dict_to_snake_dict(location) for location in locations])
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
