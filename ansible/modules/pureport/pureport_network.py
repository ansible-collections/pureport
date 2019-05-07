#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_network

short_description: Create, update or delete a network

version_added: "2.8"

description:
    - "Create, update or delete a network"

options:
    account_href:
        required: true
    id:
        description:
            - The id of the network (required if updating/deleting)
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

extends_documentation_fragment:
    - pureport_client
    - pureport_account
    - pureport_state

author:
    - Matt Traynham (@mtraynham)
'''

EXAMPLES = '''
- name: Create a network for an account
  pureport_network:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Account
  register: result  # Registers result.network

- name: Update the newly created network with changed properties
  pureport_network:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
    id: {{ result.network.id }}
    name: My Updated Ansible Account
    description: My updated ansible account description
  register: result  # Registers result.network

- name: Delete the newly created network using the 'absent' state
  pureport_network:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
    state: absent
    id: {{ result.network.id }}
    name: {{ result.network.name }}
'''

RETURN = '''
network:
    description: the created, updated, or deleted network returned from the server
    type: Network
'''

from ansible.module_utils.basic import AnsibleModule
from functools import partial
from traceback import format_exc

try:
    from pureport.exception.api import ClientHttpException, NotFoundException
except ImportError:
    ClientHttpException = None
    NotFoundException = None
from ansible.module_utils.pureport.pureport import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_client, \
    get_account_argument_spec, \
    get_account
from ansible.module_utils.pureport.pureport_crud import \
    get_state_argument_spec, \
    item_crud


def construct_network(module):
    """
    Construct a Network from the Ansible module arguments
    :param AnsibleModule module: the Ansible module
    :rtype: Network
    """
    return dict((k, module.params.get(k))
                for k in ('id', 'name', 'description'))


def retrieve_network(module, client, network):
    """
    Retrieve the Network from the Ansible inferred Network
    :param AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param Network network: the Ansible inferred Network
    :rtype: Network|None
    """
    network_id = network.get('id')
    if network_id is not None:
        try:
            return client.networks.get_by_id(network_id)
        except NotFoundException:
            return None
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())


def copy_existing_network_properties(network, existing_network):
    """
    Copy properties from the existing network to the new Ansible defined
    Network.
    :param Network network:
    :param Network existing_network:
    :rtype: Network
    """
    copied_network = dict()
    copied_network.update(network)
    copied_network.update(dict(
        href=existing_network.get('href')
    ))
    return copied_network


def create_network(module, client, network):
    """
    Create a new network
    :param AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param Network network: the Ansible inferred Network
    :rtype: Network
    """
    account = get_account(module)
    try:
        return client.accounts.networks(account).create(network)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def update_network(module, client, network):
    """
    Update a network
    :param AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param Network network: the Ansible inferred Network
    :rtype: Network
    """
    # Copy over href, the client needs it to properly execute the call
    try:
        return client.networks.update(network)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def delete_network(module, client, network):
    """
    Delete a network
    :param AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param Network network: the Ansible inferred Network
    :rtype: Network
    """
    # Copy over href, the client needs it to properly execute the call
    try:
        return client.networks.delete(network)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec(True))
    argument_spec.update(get_state_argument_spec())
    argument_spec.update(
        dict(
            id=dict(type='str'),
            name=dict(type='str', required=True),
            description=dict(type='str')
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True
    )
    client = get_client(module)
    # Using partials to fill in the method params
    (
        changed,
        changed_network,
        argument_network,
        existing_network
    ) = item_crud(
        module,
        partial(construct_network, module),
        partial(retrieve_network, module, client),
        partial(create_network, module, client),
        partial(update_network, module, client),
        partial(delete_network, module, client),
        copy_existing_item_properties_fn=copy_existing_network_properties
    )
    module.exit_json(
        changed=changed,
        network=changed_network,
        argument_network=argument_network,
        existing_network=existing_network
    )


if __name__ == '__main__':
    main()
