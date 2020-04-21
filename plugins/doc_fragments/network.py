class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    network_id:
        description:
            - The Pureport Network object's id field.
            - Only one of 'network_id' or 'network_href' should be supplied for this command.
        required: false
        type: str
    network_href:
        description:
            - The Pureport Network object's href field.
            - This should be the full 'href' path to the Network ReST object (e.g /networks/abc).
            - Only one of 'network_id' or 'network_href' should be supplied for this command.
        required: false
        type: str
    '''
