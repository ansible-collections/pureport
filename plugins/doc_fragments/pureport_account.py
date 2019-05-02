class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    account:
        description:
            - A Pureport Account object.  The dict must include an 'href' property that
            - is the location of the object on the server.
        required: false
        type: dict
    account_id:
        description:
            - A Pureport Account id.
        required: false
        type: str
    '''
