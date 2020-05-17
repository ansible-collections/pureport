# Copyright (c), Pureport, 2020
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

try:
    from pureport.api.client import Client, API_URL
    HAS_PUREPORT_CLIENT = True
except ImportError:
    HAS_PUREPORT_CLIENT = False
    API_URL = None
    Client = None


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
    client.login(
        key=module.params.get('api_key'),
        secret=module.params.get('api_secret'),
        access_token=module.params.get('api_access_token')
    )
    return client


def get_object_id(module, id_param=None, href_param=None):
    """
    Get the object id or href id from a module
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param str id_param: the id param
    :param str href_param: the href_param
    :rtype: str|None
    """
    if id_param is not None and \
            id_param in module.params and \
            module.params.get(id_param) is not None:
        return module.params.get(id_param)
    elif href_param is not None and \
            href_param in module.params and \
            module.params.get(href_param) is not None:
        href = module.params.get(href_param)
        return href.split('/')[-1]
    return None


def get_object_link(module, href_base, id_param=None, href_param=None):
    """
    Get the object id or href id from a module and build a link object for it.
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param str href_base: the base path for an href
    :param str id_param: the id param
    :param str href_param: the href_param
    :rtype: dict|None
    """
    object_id = get_object_id(module, id_param, href_param)
    if object_id is not None:
        return dict(href='%s/%s' % (href_base, object_id))
    return None


def get_account_argument_spec():
    """
    Return the basic account params
    :rtype: dict[str, dict]
    """
    return dict(
        account_href=dict(type='str'),
        account_id=dict(type='str')
    )


def get_account_mutually_exclusive():
    """
    Return the network mutually exclusive array
    :rtype: list[list[str]]
    """
    return [
        ['account_href', 'account_id']
    ]


def get_account_id(module):
    """
    Get the account id from the passed in module
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :rtype: str|None
    """
    return get_object_id(module, 'account_id', 'account_href')


def get_network_argument_spec():
    """
    Return the basic network params
    :rtype: dict[str, dict]
    """
    return dict(
        network_href=dict(type='str'),
        network_id=dict(type='str')
    )


def get_network_mutually_exclusive():
    """
    Return the network mutually exclusive array
    :rtype: list[list[str]]
    """
    return [
        ['network_href', 'network_id']
    ]


def get_network_id(module):
    """
    Get the network id from the passed in module
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :rtype: str|None
    """
    return get_object_id(module, 'network_id', 'network_href')
