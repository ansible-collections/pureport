class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    peering_type:
        description:
            - The peering type of the connection.
        required: false
        type: str
        choices: ['PRIVATE', 'PUBLIC']
        default: 'PRIVATE'
    '''
