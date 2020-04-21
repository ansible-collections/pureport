#!/usr/bin/python
#
# Copyright: Pureport
# GNU General Public License v3.0+ (see licenses/gpl-3.0-standalone.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
#
from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'Pureport'}


DOCUMENTATION = '''
---
module: aws_direct_connect_confirm_connection
short_description: Confirms the creation of the specified hosted connection on an interconnect.
description:
  - Confirms the creation of the specified hosted connection on an interconnect.
version_added: "2.8"
author: "Matt Traynham (@mtraynham)"
requirements:
  - boto3
  - botocore
options:
  connection_id:
    description:
      - The ID of the hosted connection.
    choices: [present, absent]
extends_documentation_fragment:
  - aws
  - ec2
'''

RETURN = '''
connection_state:
  description: The state of the connection.
  returned: always
  type: str
  sample: pending
'''

EXAMPLES = '''
---
- name: confirm the connection id
  aws_direct_connect_confirm_connection:
    connection_id: dxcon-XXXXXXXX
'''

from ansible.module_utils.aws.core import AnsibleAWSModule
from ansible.module_utils.aws.direct_connect import DirectConnectError
from ansible.module_utils.ec2 import (boto3_conn,
                                      ec2_argument_spec,
                                      get_aws_connection_info)


def get_connection_state(module, client, connection_id):
    try:
        return client.describe_connections(
            connectionId=connection_id
        )['connections'][0]['connectionState']
    except IndexError:
        module.fail_json(msg="Direct Connect Connection {} not found.".format(connection_id))


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
        connection_id=dict(required=True)
    ))
    module = AnsibleAWSModule(argument_spec=argument_spec)

    region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
    connection = boto3_conn(module, conn_type='client', resource='directconnect', region=region, endpoint=ec2_url, **aws_connect_kwargs)

    connection_id = module.params['connection_id']
    changed = False
    connection_state = None
    try:
        connection_state = get_connection_state(module, connection, connection_id)
        if connection_state == 'ordering':
            connection.confirm_connection(
                connectionId=module.params['connection_id']
            )
            changed = True
            connection_state = get_connection_state(module, connection, connection_id)
    except DirectConnectError as e:
        if e.exception:
            module.fail_json_aws(exception=e.exception, msg=e.msg)
        else:
            module.fail_json(msg=e.msg)

    module.exit_json(changed=changed, connection_state=connection_state)


if __name__ == '__main__':
    main()
