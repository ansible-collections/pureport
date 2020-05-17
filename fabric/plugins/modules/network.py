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
module: network
short_description: Create, update or delete a network
description:
    - "Create, update or delete a network"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    id:
        description:
            - The id of the existing network
        required: false
        type: str
    name:
        description:
            - The name of the network
        required: true
        type: str
    description:
        description:
            - A description for the network
        required: false
        type: str
    tags:
        description:
            - A map of tags to use for the connection.
            - This should be a mapping of string to string pairs with no duplicate keys.
        required: false
        type: dict
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.account
    - pureport.fabric.state
    - pureport.fabric.resolve_existing
'''

EXAMPLES = '''
- name: Create a network for an account
  network:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Account
  register: result  # Registers network as the result

- name: Update the newly created network with changed properties
  network:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
    id: "{{ result.id }}"
    name: My Updated Ansible Account
    description: My updated ansible account description
  register: result  # Registers network as the result

- name: Delete the newly created network using the 'absent' state
  network:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
    state: absent
    id: "{{ result.id }}"
    name: "{{ result.name }}"
'''

RETURN = '''
id:
    description:
        - The network id.
    returned: success
    type: str
    sample: "network-rfqj4qc9fO8hDOczEB7Z_Q"
href:
    description:
        - The network href, a path to resource on the server.
    returned: success
    type: str
    sample: "/networks/network-rfqj4qc9fO8hDOczEB7Z_Q"
name:
    description:
        - The name of the network.
    returned: success
    type: str
    sample: "My Network Name"
description:
    description:
        - The description of the network.
    returned: success
    type: str
    sample: "My network description"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
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
    get_account_argument_spec, \
    get_account_mutually_exclusive, \
    get_account_id
from ..module_utils.pureport_crud import \
    get_state_argument_spec, \
    get_resolve_existing_argument_spec, \
    item_crud


def construct_network(module):
    """
    Construct a Network from the Ansible module arguments
    :param AnsibleModule module: the Ansible module
    :rtype: pureport.api.client.Network
    """
    return dict((k, module.params.get(k))
                for k in ('id', 'name', 'description', 'tags'))


def retrieve_network(client, network):
    """
    Retrieve the Network from the Ansible inferred Network
    :param pureport.api.client.Client client: the Pureport client
    :param pureport.api.client.Network network: the Ansible inferred Network
    :rtype: pureport.api.client.Network|None
    """
    network_id = network.get('id')
    if network_id is not None:
        try:
            return client.networks.get(network_id)
        except NotFoundException:
            return None
    return None


def resolve_network(module, client, network):
    """
    Resolve the existing network from the server via some properties of the
    user provided network
    :param AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param pureport.api.client.Network network: the Ansible inferred Network
    :rtype: pureport.api.client.Network|None
    """
    account_id = get_account_id(module)
    if account_id is not None:
        existing_networks = client.accounts.networks(account_id).list()
        matched_networks = [existing_network for existing_network in existing_networks
                            if all([existing_network.get(k) == network.get(k)
                                    for k in ['name']])]
        if len(matched_networks) == 1:
            return matched_networks[0]
        elif len(matched_networks) > 1:
            module.fail_json(msg="Resolved more than one existing network.  Please provide an 'id' "
                                 "if you are attempting to update/delete an existing network.  "
                                 "Otherwise, use a more distinct name or set "
                                 "'resolve_existing' to false.")
    return None


def copy_existing_network_properties(network, existing_network):
    """
    Copy properties from the existing network to the new Ansible defined
    Network.
    :param pureport.api.client.Network network:
    :param pureport.api.client.Network existing_network:
    :rtype: pureport.api.client.Network
    """
    copied_network = dict()
    copied_network.update(network)
    copied_network.update(dict(
        id=existing_network.get('id'),
        href=existing_network.get('href')
    ))
    return copied_network


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
            tags=dict(type='dict')
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    required_one_of = []
    required_one_of += get_account_mutually_exclusive()
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
            changed_network,
            argument_network,
            existing_network
        ) = item_crud(
            module,
            partial(construct_network, module),
            partial(retrieve_network, client),
            partial(resolve_network, module, client),
            lambda network: client.accounts.networks(get_account_id(module)).create(network),
            client.networks.update,
            lambda network: client.networks.delete(network.get('id')),
            copy_existing_item_properties_fn=copy_existing_network_properties
        )
        module.exit_json(
            changed=changed,
            **camel_dict_to_snake_dict(changed_network)
        )
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


if __name__ == '__main__':
    main()
