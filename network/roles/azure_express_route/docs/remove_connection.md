# Removing a connection to Microsoft Azure

The `pureport.fabric.azure_express_route` connection role supports removing
an existing connection to Microsoft Azure.  In order to use this role to 
remove an existing connection, the registered facts (outputs) from adding
a connection are required.

To remove an existing connection, call the role with `state: absent` and pass
in the required inputs.  

## Example
```yaml
---
- hosts: localhost
  roles:
    - name: pureport.network.azure_express_route
      azure_resource_group: "{{ azure_resource_group }}"
      azure_virtual_network: "{{ azure_virtual_network }}"
      azure_express_route_circuit: "{{ azure_express_route_circuit }}"
      azure_express_route_peering: "{{ azure_express_route_peering }}"
      pureport_connection: "{{ pureport_connection }}"
      state: absent
```

## Inputs (Facts)

| Name                        | Description                                                                       | Default | Required |
| --------------------------- | --------------------------------------------------------------------------------- | ------- | -------- |
| azure_resource_group        | The output from the module `azure_rm_resourcegroup`                               | null    | yes      |
| azure_virtual_network       | The output from the module `azure_rm_virtualnetwork`                              | null    | yes      |
| azure_express_route_circuit | The output from the module `azure_rm_resource` when creating a new circuit        | null    | yes      |
| azure_express_route_peering | The output from the module `azure_rm_resource` when configing peering             | null    | yes      |
| pureport_connection         | The output from the module `pureport.fabric.azure_express_route_connection`       | null    | yes      |

## Outputs (Registered Facts)

None
