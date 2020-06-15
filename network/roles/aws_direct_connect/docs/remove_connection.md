# Removing a connection to Amazon Web Service

When setting the `state` value to `absent`, an existing connection will be 
removed.  If the connection does not exist, the role will quietly end.  For
this role to operate correctly, the input values should be the results of a
previous provisioning activity [see here](add_connection.md).

## Example
```yaml
---
- hosts: localhost

  roles:
    - name: pureport.network.aws_direct_connect
      aws_virtual_gateway: "{{ aws_virtual_gateway }}"
      aws_virtual_interfaces: "{{ aws_virtual_interfaces }}"
      aws_direct_connect_gateway: "{{ aws_direct_connect_gateway }}"
      pureport_connection: "{{ pureport_connection }}"
      state: absent
```

## Inputs (Facts)

| Name                       | Description                                                                       | Default | Required |
| -------------------------- | --------------------------------------------------------------------------------- | ------- | -------- |
| aws_virtual_gateway        | The output from the module `ec2_vpc_vgw`                                          | null    | yes      |
| aws_virtual_interfaces     | The output from the module `aws_direct_connect_virutal_interface`                 | null    | yes      |
| aws_direct_connect_gateway | The output from the module `aws_direct_connect_gateway`                           | null    | yes      |
| aws_vpc                    | The output from the module `ec2_vpc_net`                                          | null    | yes      | 
| pureport_connection        | The output from the module `pureport.fabric.google_cloud_interconnect_connection` | null    | yes      |

## Outputs (Registered Facts)

None
