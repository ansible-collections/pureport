class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    account_id:
        description:
            - The Pureport Account object's id field.
            - Only one of 'account_id' or 'account_href supplied for this command.
        required: false
        type: str
    account_href:
        description:
            - The Pureport Account object's href field.
            - This should be the full 'href' path to the Account ReST object (e.g /accounts/abc).
            - Only one of 'account_id' or 'account_href supplied for this command.
        required: false
        type: str
    '''
