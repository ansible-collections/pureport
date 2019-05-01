class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    network:
        description:
            - A Pureport Network object.  The dict must include an 'href'
            property that is the location of the object on the server.
        required: false
        type: dict
    network_id:
        description:
            - A Pureport Network id.
        required: false
        type: str
    '''