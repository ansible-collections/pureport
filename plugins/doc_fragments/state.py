class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    state:
        description:
            - The state of the object, where 'present' indicates it should should
            - exist and 'absent' indicates it should not exist.
        required: false
        type: str
        choices: ['present', 'absent']
        default: 'present'
    '''
