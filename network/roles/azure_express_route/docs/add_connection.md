# Adding a connection to Microsoft Azure

The `pureport.fabric.azure_express_route` role allows you to add a new 
connection to a Pureport network over ExpressRoute.  To add a new connnection
simply call the role from your Ansible playbook and the connection will 
be created.  Optionally, you can add `state: present` to your play as well.

## Example

```yaml
---
- hosts: localhost
  roles:
    - name: pureport.network.azure_express_route
      azure_rg_name: pureport-rg
      azure_location: washington_dc
      azure_vnet_name: pureport-vnet
      azure_circuit_name: pureport-circuit
      pureport_network_name: default
      pureport_connection_speed: 50
      pureport_connection_name: azure-gateway
      state: present
```

## Inputs (Facts)

| Name                        | Description                                                                                                                                                       | Default            | Required |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | -------- |
| azure_rg_name               | The name of the Azure Resource Group to be created                                                                                                                | `pureport-rg`      | no       |
| azure_location              | The name of the Azure location where the ExpressRoute circuit is created.  Valid values include `chicago`, `dallas`, `seattle`, `silicon_valley`, `washington_dc` | null               | yes      |
| azure_vnet_name             | The name of the Azure virtual network instance to be created                                                                                                      | `pureport-vnet`    | no       |
| azure_vnet_cidr             | The subnet in `a.b.c.d./e` notation associated with this virutal network                                                                                          | `10.0.0.0/16`      | no       |
| azure_circuit_name          | The name of the Azure ExpressRoute circuit to be created                                                                                                          | `pureport-circuit` | no       |
| pureport_network_name       | The name o the Pureport network to be created                                                                                                                     | `default`          | no       |
| pureport_network_descriptio | Short description associated with the Pureport network                                                                                                            | null               | no       |
| pureport_connection_name    | The name of the Pureport connection to be created                                                                                                                 | `azure-gateway`    | no       |
| pureport_connection_speed   | The speed in Mbps of the Pureport connection.  Value values include `50`, `100`, `200`, `500`, `1000`, `2000`, `5000`, `10000`                                    | null               | yes      |


## Outputs (Registered Facts)

| Name                        | Description                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| azure_resource_group        | The output from the module `azure_rm_resourcegroup`                         |
| azure_virtual_network       | The output from the module `azure_rm_virtualnetwork`                        |
| azure_express_route_circuit | The output from the module `azure_rm_resource` when creating the circuit    |
| azure_express_route_peering | The output from the module `azure_rm_resource` when configuring peering     |
| pureport_network            | The output from the module `pureport.fabric.network`                        |
| pureport_connection         | The output from the module `pureport.fabric.azure_express_route_connection` |
