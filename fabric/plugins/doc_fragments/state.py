# Copyright (c), Pureport, 2020
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


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
