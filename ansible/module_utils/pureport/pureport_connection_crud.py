from functools import partial
from traceback import format_exc
try:
    from pureport.exception.api import ClientHttpException, NotFoundException
except ImportError:
    ClientHttpException = None
    NotFoundException = None
from ansible.module_utils.pureport.pureport import get_client, get_network
from ansible.module_utils.pureport.pureport_crud import item_crud, deep_compare


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
        location_href=dict(type='str', required=True),
        billing_term=dict(type='str', required=True, choices=['HOURLY']),
        cloud_services=dict(type='list'),
        customer_asn=dict(type='int'),
        customer_networks=dict(type='list', default=[]),
        nat_enabled=dict(type='bool', default=False),
        nat_mappings=dict(type='list', default=[])
    )


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


def __retrieve_connection(module, client, connection):
    """
    Retrieve the Connection from the Ansible inferred Connection
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param Connection connection: the Ansible inferred Connection
    :rtype: Connection|None
    """
    connection_id = connection.get('id')
    if connection_id is not None:
        try:
            return client.connections.get_by_id(connection_id)
        except NotFoundException:
            return None
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())
    return None


def __resolve_connection(module, client, connection):
    """
    Resolve the existing connection from the server via some properties of the
    user provided connection
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param Connection connection: the Ansible inferred Connection
    :rtype: Connection|None
    """
    network = get_network(module)
    if network is not None:
        try:
            existing_connections = client.networks.connections(network).list()
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
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())
    return None


def __copy_existing_connection_properties(connection, existing_connection):
    """
    Copy properties from the existing connection to the new Ansible defined
    Connection, notably the network and the href.
    :param Connection connection:
    :param Connection existing_connection:
    :rtype: Connection
    """
    copied_connection = dict()
    copied_connection.update(connection)
    copied_connection.update(dict(
        id=existing_connection.get('id'),
        network=existing_connection.get('network'),
        href=existing_connection.get('href')
    ))
    return copied_connection


def __create_connection(module, client, wait_for_server, connection):
    """
    Create a new connection
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param bool wait_for_server: should the client wait for the server to finish
    :param Connection connection: the Ansible inferred Connection
    :rtype: Connection
    """
    network = get_network(module)
    try:
        return client.networks.connections(network).create(connection, wait_until_active=wait_for_server)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def __update_connection(module, client, wait_for_server, connection):
    """
    Update a Connection
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param bool wait_for_server: should the client wait for the server to finish
    :param Connection connection: the Ansible inferred Connection
    :rtype: Connection
    """
    try:
        return client.connections.update(connection, wait_until_active=wait_for_server)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def __delete_connection(module, client, wait_for_server, connection):
    """
    Delete a connection
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param bool wait_for_server: should the client wait for the server to finish
    :param Connection connection: the Ansible inferred Connection
    :rtype: Connection
    """
    try:
        return client.connections.delete(connection, wait_until_deleted=wait_for_server)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


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
        partial(__retrieve_connection, module, client),
        partial(__resolve_connection, module, client),
        partial(__create_connection, module, client, wait_for_server),
        partial(__update_connection, module, client, wait_for_server),
        partial(__delete_connection, module, client, wait_for_server),
        compare_item_fn=compare_item_fn,
        copy_existing_item_properties_fn=__copy_existing_connection_properties
    )
