# Copyright (c), Pureport, 2020
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


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
