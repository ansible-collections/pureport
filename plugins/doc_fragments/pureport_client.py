class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    api_base_url:
        description:
            - The host url for the Pureport API.
        required: false
        type: str
    api_key:
        description:
            - The pre-configured API Key for a Pureport Account.
        required: true
        type: str
    api_secret:
        description:
            - The pre-configured API Secret for a Pureport Account.
        required: true
        type: str
    '''
