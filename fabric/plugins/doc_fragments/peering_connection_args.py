# Copyright (c), Pureport, 2020
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


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
