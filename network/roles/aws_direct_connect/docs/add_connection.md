# Adding a connection to Amazon Web Service

When setting the `state` value to `present` (default), a new connection will
be added between Pureport and Amazon Web Service, if the connection does not 
already exist.  

The closest Pureport location is automatically selected based on the AWS region.

## Example

The example below shows the minimum necessary to create a new connection from 
Pureport to AWS using Direct Connect

```yaml
---
- hosts: localhost

  roles:
    - name: pureport.network.aws_direct_connect
      aws_region: us-west-1
      pureport_connection_speed: 50
      state: present
```

## Inputs (Facts)

| Name                         | Description                                                    | Default     | Required |
| ---------------------------- | -------------------------------------------------------------- | ----------- | -------- |
| aws_region                   | The AWS region where this connection should be created         | null        | yes      |
| aws_vpc_name                 | The name of the AWS VPC to be created                          | `pureport-vpc`         | no       |
| aws_vpc_cidr_block           | The CIDR block in `a.b.c.d/e` notation associated with the VPC | `10.0.0.0/16` | no       |
| aws_vgw_name                 | The name of the AWS VGW to be created                          | `pureport-vgw`         | no       |
| aws_manage_vpc               | Flag that indicates if the AWS VPC and VGW should be created   | no          | no       |
| aws_dcg_name                 | The name of the AWS Direct Connect gateway to be created       | `pureport-dcg`         | no       |
| aws_vif_name                 | The name of the AWS virtual interface to be created.  The name will be appended with a `-1` and `-2` to indicate the primary and secondary interfaces.            | `pureport-vif`         | no       |
| pureport_network_name        | The name of the Pureport network to be created                 | `default`     | no       |
| pureport_network_description | Short description associated with the Pureport network         | `Automatically created by Ansible`        | no       |
| pureport_connection_name     | The name of the Pureport connection to be created              | `aws-gateway`     | no       |
| pureport_connection_speed    | The speed in Mbps of the Pureport connection to be created.  Must be one of `50`, `100`, `200`, `300`, `400`, `500`, `1000`, `2000`, `5000`, `10000`            | null        | yes      |


## Outputs (Registered Facts)

| Name                       | Description                                                            |
| -------------------------- | ---------------------------------------------------------------------- |
| aws_vpc                    | The output from `ec2_vpc_net`                                          |
| aws_virtual_gateway        | The output from `ec2_vpc_vgw`                                          |
| aws_direct_connect_gateway | The output from `aws_direct_connect_gateway`                           |
| aws_virtual_interfaces     | The ouput from `pureport.fabric.direct_connect_virtual_interface`      |
| pureport_network           | The output from `pureport.fabric.pureport_network`                     |
| pureport_connection        | The output from `pureport.fabric.aws_direct_connect_connection`        |
| pureport_gateways          | Primary and secondary gateways associated with the Pureport connection |

