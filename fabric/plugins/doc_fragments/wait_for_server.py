# Copyright (c), Pureport, 2020
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    wait_for_server:
        description:
            - These create/update/delete calls are typically async.  If you wish to wait until the
            - server has completed it's task, set this to True.
        required: false
        type: bool
    '''
