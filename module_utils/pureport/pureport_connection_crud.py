from functools import partial
from traceback import format_exc
try:
    from pureport.exception.api import ClientHttpException, NotFoundException
except ImportError:
    pass
from ansible.module_utils.pureport import get_client, get_network
from ansible.module_utils.pureport_crud import item_crud, deep_compare


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
        id=dict(type="str"),
        name=dict(type="str", required=True),
        description=dict(type="str"),
        speed=dict(type="int", required=True, choices=[50, 100, 200, 300, 400, 500, 1000, 1000]),
        high_availability=dict(type="bool"),
        location=dict(type="dict", required=True),
        billing_term=dict(type="str", required=True, choices=['HOURLY']),
        cloud_services=dict(type="list"),
        customerASN=dict(type="long"),
        customer_networks=dict(type="list", default=[]),
        nat=dict(type="dict")
    )


def get_peering_connection_argument_spec():
    """
    Return basic params for a connection
    :rtype: dict[str, dict]
    """
    return dict(
        peering_type=dict(type="str", choices=['PRIVATE', 'PUBLIC'], default='PRIVATE'),
        name=dict(type="str", required=True),
        description=dict(type="str"),
        speed=dict(type="int", required=True, choices=[50, 100, 200, 300, 400, 500, 1000, 1000]),
        high_availability=dict(type="bool"),
        location=dict(type="dict", required=True),
        billing_term=dict(type="str", required=True, choices=['HOURLY']),
        cloud_services=dict(type="list"),
        customerASN=dict(type="long"),
        customer_networks=dict(type="list", default=[]),
        nat=dict(type="dict")
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


def __create_connection(module, client, wait_for_server, connection):
    """
    Create a new connection
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param bool wait_for_server: should the client wait for the server to finish
    :param Connection connection: the Ansible inferred Connection
    :rtype: Connection
    """
    network = get_network(module, client)
    try:
        return client.networks.connections(network).create(connection, wait_until_active=wait_for_server)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def __update_connection(module, client, wait_for_server, connection, existing_connection):
    """
    Update a Connection
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param bool wait_for_server: should the client wait for the server to finish
    :param Connection connection: the Ansible inferred Connection
    :param Connection existing_connection: the Connection obtained from the server
    :rtype: Connection
    """
    # Copy over href, the client needs it to properly execute the call
    connection['href'] = existing_connection['href']
    try:
        return client.connections.update(connection, wait_until_active=wait_for_server)
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())


def __delete_connection(module, client, wait_for_server, connection, existing_connection):
    """
    Delete a connection
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param pureport.api.client.Client client: the Pureport client
    :param bool wait_for_server: should the client wait for the server to finish
    :param Connection connection: the Ansible inferred Connection
    :param Connection existing_connection: the Connection obtained from the server
    :rtype: Connection
    """
    # Copy over href, the client needs it to properly execute the call
    connection['href'] = existing_connection['href']
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
        partial(__create_connection, module, client, wait_for_server),
        partial(__update_connection, module, client, wait_for_server),
        partial(__delete_connection, module, client, wait_for_server),
        compare_item_fn
    )
