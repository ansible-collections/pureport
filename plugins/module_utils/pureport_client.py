# Copyright (c), Pureport, 2020
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from traceback import format_exc

try:
    from pureport.api.client import Client, API_URL
    from pureport.exception.api import ClientHttpException
    HAS_PUREPORT_CLIENT = True
except ImportError:
    HAS_PUREPORT_CLIENT = False
    Client = None
    ClientHttpException = None


def get_client_argument_spec():
    """
    Return the basic client params
    :rtype: dict[str, dict]
    """
    return dict(
        api_base_url=dict(type='str', default=API_URL),
        api_key=dict(type='str'),
        api_secret=dict(type='str', no_log=True),
        api_access_token=dict(type='str', no_log=True)
    )


def get_client_mutually_exclusive():
    """
    Return the basic client mutually exclusive array
    :rtype: list[list[str]]
    """
    return [
        ['api_key', 'api_access_token'],
        ['api_secret', 'api_access_token']
    ]


def get_client(module):
    """
    Get a Pureport Client instance
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :rtype: Client
    """
    if not HAS_PUREPORT_CLIENT:
        module.fail_json(msg='pureport-client required for this module')
    client = Client(module.params.get('api_base_url'))
    try:
        client.login(
            key=module.params.get('api_key'),
            secret=module.params.get('api_secret'),
            access_token=module.params.get('api_access_token')
        )
    except ClientHttpException as e:
        module.fail_json(msg=e.response.text, exception=format_exc())
    return client


def get_account_argument_spec(required=False):
    """
    Return the basic account params
    :param bool required: are these params required
    :rtype: dict[str, dict]
    """
    return dict(
        account_href=dict(type='str', required=required)
    )


def get_account(module):
    """
    Get the account from the passed in module
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :rtype: Account|None
    """
    account_href = module.params.get('account_href')
    return dict(href=account_href) if account_href is not None else None


def get_network_argument_spec(required=False):
    """
    Return the basic account params
    :param bool required: are these params required
    :rtype: dict[str, dict]
    """
    return dict(
        network_href=dict(type='str', required=required)
    )


def get_network(module):
    """
    Get the account from the passed in module
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :rtype: Network|None
    """
    network_href = module.params.get('network_href')
    return dict(href=network_href) if network_href is not None else None
