# Copyright (c), Pureport, 2020
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    resolve_existing:
        description:
            - If an id was not provided, attempt to resolve the existing item using the name.
        required: false
        type: bool
        default: true
    '''
