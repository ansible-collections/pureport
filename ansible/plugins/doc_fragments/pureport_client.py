class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    api_base_url:
        description:
            - The host url for the Pureport API.
        required: false
        type: str
    api_access_token:
        description:
            - The access token to use with Pureport API.  This can be obtained from
            - the `pureport_access_token_fact` module.
        required: true
        type: str
    '''
