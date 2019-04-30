#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: pureport_network

short_description: Create, update or delete a Network

version_added: "2.7"

description:
    - "Create, update or delete a Network"

options:
    api_base_url:
        description:
            - The host url for the Pureport API
        required: false
        type: str
    api_key:
        description:
            - This is the pre-configured API Key for a Pureport Account
        required: true
        type: str
    api_secret:
        description:
            - This is the pre-configured API Secret for a Pureport Account
        required: true
        type: str
    account:
        description:
            - The account for newly created networks
        required: false
        type: dict
    account_id:
        description:
            - The account id for newly created networks
        required: false
        type: str
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
    - pureport

author:
    - Matt Traynham (@mtraynham)
'''

EXAMPLES = '''
'''

RETURN = '''
network:
    description: the created, updated, or deleted network
    type: Network
'''

from ansible.module_utils.basic import AnsibleModule
from functools import partial
from traceback import format_exc

try:
    from pureport.exception.api import ClientHttpException, NotFoundException
except ImportError:
    pass
from module_utils.pureport import \
    get_client_argument_spec, \
    get_client, \
    get_account_argument_spec, \
    get_account_mutually_exclusive, \
    get_account
from module_utils.pureport_crud import item_crud


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


def create_network(module, client, network):
    """
    Create a new network
    :param AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param Network network: the Ansible inferred Network
    :rtype: Network
    """
    account = get_account(module, client)
    try:
        return client.accounts.networks(account).create(network)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def update_network(module, client, network, existing_network):
    """
    Update a network
    :param AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param Network network: the Ansible inferred Network
    :param Network existing_network: the network obtained from the server
    :rtype: Network
    """
    # Copy over href, the client needs it to properly execute the call
    network['href'] = existing_network['href']
    try:
        return client.networks.update(network)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def delete_network(module, client, network, existing_network):
    """
    Delete a network
    :param AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param Network network: the Ansible inferred Network
    :param Network existing_network: the network obtained from the server
    :rtype: Network
    """
    # Copy over href, the client needs it to properly execute the call
    network['href'] = existing_network['href']
    try:
        return client.networks.delete(network)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec())
    argument_spec.update(
        dict(
            id=dict(type="str"),
            name=dict(type="str"),
            description=dict(type="str")
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_account_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True
    )
    client = get_client(module)
    # Using partials to fill in the method params
    (changed, changed_network, network, existing_network) = item_crud(
        module,
        partial(construct_network, module),
        partial(retrieve_network, module, client),
        partial(create_network, module, client),
        partial(update_network, module, client),
        partial(delete_network, module, client)
    )
    module.exit_json(changed=changed, network=changed_network)


if __name__ == '__main__':
    main()
