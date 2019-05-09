class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    resolve_existing:
        description:
            - If an id was not provided, attempt to resolve the existing item
            - via some of the provided properties.
        required: false
        type: bool
        default: true
    '''
