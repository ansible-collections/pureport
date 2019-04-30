from traceback import format_exc
try:
    from pureport.api.client import Client
    from pureport.exception.api import ClientHttpException
    HAS_PUREPORT_CLIENT = True
except ImportError:
    HAS_PUREPORT_CLIENT = False


def get_client_argument_spec():
    """
    Return the basic account params
    :rtype: dict[str, dict]
    """
    return dict(
        api_base_url=dict(type='str'),
        api_key=dict(type='str', required=True),
        api_secret=dict(type='str', required=True, no_log=True)
    )


def get_client(module):
    """
    Get a Pureport Client instance
    :param AnsibleModule module: the Ansible module
    :rtype: Client
    """
    if not HAS_PUREPORT_CLIENT:
        module.fail_json(msg='pureport-client required for this module')
    client = Client(module.params.get('api_base_url'))
    try:
        client.login(module.params.get('api_key'), module.params.get('api_secret'))
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())
    return client


def get_account_argument_spec():
    """
    Return the basic account params
    :rtype: dict[str, dict]
    """
    return dict(
        account=dict(type='dict'),
        account_id=dict(type='str')
    )


def get_account_mutually_exclusive():
    """
    Return the basic account mutually exclusive params
    :rtype: list[list[str]]
    """
    return [
        ['account', 'account_id']
    ]


def get_account(module, client):
    """
    Get the account from the passed in module
    :param AnsibleModule module: the Ansible module
    :param Client client: the Pureport client
    :rtype: Account
    """
    account = module.params.get('account')
    if not account:
        account_id = module.params.get('account_id')
        if account_id is not None:
            try:
                account = client.accounts.get_by_id(account_id)
            except ClientHttpException as e:
                module.fail_json(msg=e.response.text, exception=format_exc())
        else:
            module.fail_json(msg='missing account or account_id parameter')
    return account


def get_network_argument_spec():
    """
    Return the basic account params
    :rtype: dict[str, dict]
    """
    return dict(
        network=dict(type='dict'),
        network_id=dict(type='str')
    )


def get_network_mutually_exclusive():
    """
    Return the basic account mutually exclusive params
    :rtype: list[list[str]]
    """
    return [
        ['network', 'network_id']
    ]


def get_network(module, client):
    """
    Get the account from the passed in module
    :param AnsibleModule module: the Ansible module
    :param Client client: the Pureport client
    :rtype: Network
    """
    network = module.params.get('network')
    if not network:
        network_id = module.params.get('network_id')
        if network_id is not None:
            try:
                network = client.networks.get_by_id(network_id)
            except ClientHttpException as e:
                module.fail_json(msg=e.response.text, exception=format_exc())
        else:
            module.fail_json(msg='missing network or network_id parameter')
    return network
