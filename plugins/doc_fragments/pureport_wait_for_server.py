class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    wait_for_server:
        description:
            - These create/update/delete calls are typically async.  If you 
            wish to wait until the server has completed it's task.  Set this to True.
        required: false,
        type: bool
    '''