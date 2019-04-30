from traceback import format_exc
try:
    from pureport.exception.api import ClientHttpException, NotFoundException
except ImportError:
    pass
from module_utils.pureport import get_client, get_network
from module_utils.pureport_crud import item_crud, deep_compare


def connection_crud(module,
                    construct_item_fn,
                    compare_item_fn=deep_compare):
    """
    Handle a basic connection's Ansible CRUD operations
    :param AnsibleModule module: the Ansible module
    :param () -> T construct_item_fn:
        A function that creates the item from the Ansible module params
    :param (T, T) -> boolean compare_item_fn:
        A function that compares the Ansible item with the retrieved item
    :rtype: (bool, T, T, T)
    """
    client = get_client(module)

    def retrieve_connection(connection):
        """
        Retrieve the Connection from the Ansible inferred Connection
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

    def create_connection(connection):
        """
        Create a new connection
        :param Connection connection: the Ansible inferred Connection
        :rtype: Connection
        """
        network = get_network(module, client)
        try:
            return client.networks.connections(network).create(connection)
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())

    def update_connection(connection, existing_connection):
        """
        Update a network
        :param Connection connection: the Ansible inferred Connection
        :param Connection existing_connection: the Connection obtained from the server
        :rtype: Connection
        """
        # Copy over href, the client needs it to properly execute the call
        connection['href'] = existing_connection['href']
        try:
            return client.connections.update(connection)
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())

    def delete_connection(connection, existing_connection):
        """
        Delete a connection
        :param Connection connection: the Ansible inferred Connection
        :param Connection existing_connection: the Connection obtained from the server
        :rtype: Network
        """
        # Copy over href, the client needs it to properly execute the call
        connection['href'] = existing_connection['href']
        try:
            return client.connections.delete(connection)
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())

    return item_crud(
        module,
        construct_item_fn,
        retrieve_connection,
        create_connection,
        update_connection,
        delete_connection,
        compare_item_fn
    )