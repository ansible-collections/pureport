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
module: port
short_description: Create, update or delete a port
description:
    - "Create, update or delete a port"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    id:
        description:
            - The id of the existing port
        required: false
        type: str
    name:
        description:
            - The name of the port
        required: true
        type: str
    description:
        description:
            - A description for the port
        required: false
        type: str
    facility_id:
        description:
            - The Pureport Facility id.
            - Only one of 'facility_id' or 'facility_href' can be supplied for this command.
        required: false
        type: str
    facility_href:
        description:
            - The Pureport Facility href.
            - This should be the full 'href' path to the Facility ReST object (e.g /facilities/abc).
            - Only one of 'facility_id' or 'facility_href' can be supplied for this command.
        required: false
        type: str
    provider:
        description:
            - The port provider
        required: true
        type: str
    speed:
        description:
            - A speed for the port
        required: true
        type: int
        choices: [1000, 10000, 40000]
    media_type:
        description:
            - A media type for the port
        required: true
        type: str
    availability_domain:
        description:
            - An availabiliy domain for the port
        required: true
        type: str
        choices: ['PRIMARY', 'SECONDARY']
    billing_term:
        description:
            - A billign term for the port
        required: true
        type: str
        choices: ['HOURLY', 'MONTHLY', 'ONE_YEAR', 'TWO_YEAR']
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.account
    - pureport.fabric.state
    - pureport.fabric.resolve_existing
'''

EXAMPLES = '''
- name: Create a port for an account
  port:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
    facility_href: /facilities/fac-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Port
    speed: 1000
    media_type: LX
    availability_domain: PRIMARY
    billing_term: MONTHLY
  register: result  # Registers network as the result

- name: Update the newly created port with changed properties
  network:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
    facility_href: /facilities/fac-XXXXXXXXXXXXXXXXXXXXXX
    id: "{{ result.id }}"
    name: My Ansible Port 2
    speed: "{{ result.speed }}"
    media_type: "{{ result.media_type }}"
    availability_domain: "{{ result.availability_domain }}"
    billing_term: "{{ result.billing_term}}"
  register: result  # Registers network as the result

- name: Delete the newly created port using the 'absent' state
  network:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
    facility_href: /facilities/fac-XXXXXXXXXXXXXXXXXXXXXX
    state: absent
    id: "{{ result.id }}"
    name: "{{ result.name }}"
    speed: "{{ result.speed }}"
    media_type: "{{ result.media_type }}"
    availability_domain: "{{ result.availability_domain }}"
    billing_term: "{{ result.billing_term}}"
'''

RETURN = '''
id:
    description:
        - The port id.
    returned: success
    type: str
    sample: "port-rfqj4qc9fO8hDOczEB7Z_Q"
href:
    description:
        - The port href, a path to resource on the server.
    returned: success
    type: str
    sample: "/ports/port-rfqj4qc9fO8hDOczEB7Z_Q"
account:
    description:
        - The account this port is tied to.
    returned: success
    type: complex
    contains:
        id:
            description:
                - The account id
            returned: success
            type: str
            sample: "ac-XXXXXXXXXXXXXXXXXXXXXX"
        href:
            description:
                - The account href
            returned: success
            type: str
            sample: "/accounts/ac-XXXXXXXXXXXXXXXXXXXXXX"
        title:
            description:
                - The account title
            returned: success
            type: str
            sample: "My Account"
facility:
    description:
        - The facility this port is tied to.
    returned: success
    type: complex
    contains:
        id:
            description:
                - The facility id
            returned: success
            type: str
            sample: "fac-XXXXXXXXXXXXXXXXXXXXXX"
        href:
            description:
                - The facility href
            returned: success
            type: str
            sample: "/facilities/fac-XXXXXXXXXXXXXXXXXXXXXX"
        title:
            description:
                - The facility title
            returned: success
            type: str
            sample: "My Facility"
name:
    description:
        - The name of the port.
    returned: success
    type: str
    sample: "My Port Name"
description:
    description:
        - The description of the port.
    returned: success
    type: str
    sample: "My port description"
provider:
    description:
        - The port provider
    returned: success
    type: str
    sample: PACKET_FABRIC
speed:
    description:
        - The speed of the port.
    returned: success
    type: int
    sample: 1000
media_type:
    description:
        - The media type of the port.
    returned: success
    type: str
    sample: LX
availability_domain:
    description:
        - The availability domain of the port.
    returned: success
    type: str
    sample: PRIMARY
billing_term:
    description:
        - The billing term of the port.
    returned: success
    type: str
    sample: MONTHLY
state:
    description:
        - The state of the port.
    returned: success
    type: str
    sample: ACTIVE
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import \
    camel_dict_to_snake_dict, \
    snake_dict_to_camel_dict
from functools import partial
from traceback import format_exc

try:
    from pureport.exception.api import ClientHttpException, NotFoundException
except ImportError:
    ClientHttpException = None
    NotFoundException = None
from ..module_utils.pureport_client import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_client, \
    get_object_link, \
    get_account_argument_spec, \
    get_account_mutually_exclusive, \
    get_account_id
from ..module_utils.pureport_crud import \
    get_state_argument_spec, \
    get_resolve_existing_argument_spec, \
    item_crud


def construct_port(module):
    """
    Construct a Port from the Ansible module arguments
    :param AnsibleModule module: the Ansible module
    :rtype: Port
    """
    port = dict()
    port.update(dict((k, module.params.get(k))
                     for k in ('id', 'name', 'description',
                               'provider', 'speed', 'media_type',
                               'availability_domain', 'billing_term')))
    port.update(dict(
        account=get_object_link(module, '/accounts', 'account_id', 'account_href'),
        facility=get_object_link(module, '/facilities', 'facility_id', 'facility_href'),
    ))
    port = snake_dict_to_camel_dict(port)
    return port


def retrieve_port(client, port):
    """
    Retrieve the Port from the Ansible inferred Port
    :param pureport.api.client.Client client: the Pureport client
    :param Port port: the Ansible inferred Port
    :rtype: Port|None
    """
    port_id = port.get('id')
    if port_id is not None:
        try:
            return client.ports.get(port_id)
        except NotFoundException:
            return None
    return None


def resolve_port(module, client, port):
    """
    Resolve the existing port from the server via some properties of the
    user provided port
    :param AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param Port port: the Ansible inferred Port
    :rtype: Port|None
    """
    account_id = get_account_id(module)
    if account_id is not None:
        existing_ports = client.accounts.ports(account_id).list()
        matched_ports = [existing_port for existing_port in existing_ports
                         if all([existing_port.get(k) == port.get(k)
                                 for k in ['name']])]
        if len(matched_ports) == 1:
            return matched_ports[0]
        elif len(matched_ports) > 1:
            module.fail_json(msg="Resolved more than one existing port.  Please provide an 'id' "
                                 "if you are attempting to update/delete an existing port.  "
                                 "Otherwise, use a more distinct name or set "
                                 "'resolve_existing' to false.")
    return None


def copy_existing_port_properties(port, existing_port):
    """
    Copy properties from the existing port to the new Ansible defined
    Port.
    :param Port port:
    :param Port existing_port:
    :rtype: Port
    """
    copied_port = dict()
    copied_port.update(port)
    copied_port.update(dict(
        id=existing_port.get('id'),
        href=existing_port.get('href')
    ))
    return copied_port


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec())
    argument_spec.update(get_state_argument_spec())
    argument_spec.update(get_resolve_existing_argument_spec())
    argument_spec.update(
        dict(
            id=dict(type='str'),
            name=dict(type='str', required=True),
            description=dict(type='str'),
            facility_id=dict(type='str'),
            facility_href=dict(type='str'),
            provider=dict(type='str', required=True),
            speed=dict(type='int', required=True, choices=[1000, 10000, 40000]),
            media_type=dict(type='str', required=True),
            availability_domain=dict(type='str', required=True, choices=['PRIMARY', 'SECONDARY']),
            billing_term=dict(type='str', required=True, choices=['HOURLY', 'MONTHLY', 'ONE_YEAR', 'TWO_YEAR'])
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    required_one_of = []
    required_one_of += get_account_mutually_exclusive()
    required_one_of += [
        ['facility_id', 'facility_href']
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        required_one_of=required_one_of,
        supports_check_mode=True
    )
    # Using partials to fill in the method params
    try:
        client = get_client(module)
        (
            changed,
            changed_port,
            argument_port,
            existing_port
        ) = item_crud(
            module,
            partial(construct_port, module),
            partial(retrieve_port, client),
            partial(resolve_port, module, client),
            lambda port: client.accounts.ports(get_account_id(module)).create(port),
            client.ports.update,
            lambda port: client.ports.delete(port.get('id')),
            copy_existing_item_properties_fn=copy_existing_port_properties
        )
        module.exit_json(
            changed=changed,
            **camel_dict_to_snake_dict(changed_port)
        )
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
