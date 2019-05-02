class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    peering_type:
        description:
            - The peering type of the connection.
        required: true
        type: str
        choices: ['PRIVATE', 'PUBLIC']
    '''