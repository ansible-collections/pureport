# Copyright (c), Pureport, 2020
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from functools import partial

try:
    from pureport.exception.api import ClientHttpException, NotFoundException
except ImportError:
    ClientHttpException = None
    NotFoundException = None

from .pureport_client import get_client, get_network_id
from .pureport_crud import item_crud, deep_compare


def get_wait_for_server_argument_spec():
    """
    Return the basic wait_for_server param
    :rtype: dict[str, dict]
    """
    return dict(
        wait_for_server=dict(type='bool', default=False)
    )


def get_connection_argument_spec():
    """
    Return basic params for a connection
    :rtype: dict[str, dict]
    """
    return dict(
        id=dict(type='str'),
        name=dict(type='str', required=True),
        description=dict(type='str'),
        speed=dict(type='int', required=True, choices=[50, 100, 200, 300, 400, 500, 1000, 1000]),
        high_availability=dict(type='bool'),
        location_id=dict(type='str'),
        location_href=dict(type='str'),
        billing_term=dict(type='str', choices=['HOURLY', 'MONTHLY', 'ONE_YEAR', 'TWO_YEAR'], default='HOURLY'),
        customer_asn=dict(type='int'),
        customer_networks=dict(type='list', default=[], elements='dict'),
        nat_enabled=dict(type='bool', default=False),
        nat_mappings=dict(type='list', default=[], elements='str'),
        tags=dict(type='dict')
    )


def get_connection_required_one_of():
    """
    Return the connection required one of array
    :rtype: list[list[str]]
    """
    return [
        ['location_id', 'location_href']
    ]


def get_cloud_connection_argument_spec():
    """
    Return basic params for a cloud connection
    :rtype: dict[str, dict]
    """
    return dict()


def get_peering_connection_argument_spec():
    """
    Return basic params for a peering connection
    :rtype: dict[str, dict]
    """
    return dict(
        peering_type=dict(type='str', choices=['PRIVATE', 'PUBLIC'], default='PRIVATE'),
    )


def __retrieve_connection(client, connection):
    """
    Retrieve the Connection from the Ansible inferred Connection
    :param pureport.api.client.Client client: the Pureport client
    :param pureport.api.client.Connection connection: the Ansible inferred Connection
    :rtype: pureport.api.client.Connection |None
    """
    connection_id = connection.get('id')
    if connection_id is not None:
        try:
            return client.connections.get(connection_id)
        except NotFoundException:
            return None
    return None


def __resolve_connection(module, client, connection):
    """
    Resolve the existing connection from the server via some properties of the
    user provided connection
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param pureport.api.client.Connection connection: the Ansible inferred Connection
    :rtype: pureport.api.client.Connection|None
    """
    network_id = get_network_id(module)
    if network_id is not None:
        existing_connections = client.networks.connections(network_id).list()
        matched_connections = [existing_connection for existing_connection in existing_connections
                               if all([existing_connection.get(k) == connection.get(k)
                                       for k in ['name', 'type']])]
        if len(matched_connections) == 1:
            return matched_connections[0]
        elif len(matched_connections) > 1:
            module.fail_json(msg="Resolved more than one existing connection.  Please provide an 'id' "
                                 "if you are attempting to update/delete an existing connection.  "
                                 "Otherwise, use a more distinct name & type or set "
                                 "'resolve_existing' to false.")
    return None


def __copy_existing_connection_properties(connection, existing_connection):
    """
    Copy properties from the existing connection to the new Ansible defined
    Connection, notably the network and the href.
    :param pureport.api.client.Connection connection:
    :param pureport.api.client.Connection existing_connection:
    :rtype: pureport.api.client.Connection
    """
    copied_connection = dict()
    copied_connection.update(connection)
    copied_connection.update(dict(
        id=existing_connection.get('id'),
        network=existing_connection.get('network'),
        href=existing_connection.get('href')
    ))
    return copied_connection


def connection_crud(module,
                    construct_item_fn,
                    compare_item_fn=deep_compare):
    """
    Handle a basic connection's Ansible CRUD operations
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param () -> T construct_item_fn:
        A function that creates the item from the Ansible module params
    :param (T, T) -> boolean compare_item_fn:
        A function that compares the Ansible item with the retrieved item
    :rtype: (bool, T, T, T)
    """
    client = get_client(module)
    wait_for_server = module.params.get('wait_for_server')
    return item_crud(
        module,
        construct_item_fn,
        partial(__retrieve_connection, client),
        partial(__resolve_connection, module, client),
        lambda connection: client.networks
                                 .connections(get_network_id(module))
                                 .create(connection, wait_until_active=wait_for_server),
        lambda connection: client.connections.update(connection, wait_until_active=wait_for_server),
        lambda connection: client.connections.delete(connection.get('id'), wait_until_deleted=wait_for_server),
        compare_item_fn=compare_item_fn,
        copy_existing_item_properties_fn=__copy_existing_connection_properties
    )
