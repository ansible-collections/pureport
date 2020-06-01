# Removing a connection to Google Cloud

When setting the `state` value to `absent`, an existing connection will be 
removed.  If the connection does not exist, the role will quietly end.  For
this role to operate correctly, the input values should be the results of a
previous provisioning activity [see here](add_connection.md).

## Example
```yaml
---
- hosts: localhost

  roles:
    - name: pureport.network.google_cloud_interconnect
      gcp_network: "{{ gcp_network_result }}"
      gcp_routers: "{{ gcp_routers_result }}"
      gcp_attachments: "{{ gcp_attachments_result }}"
      pureport_network: "{{ pureport_network_result }}"
      pureport_connection: "{{ pureport_connection_result}}"
      state: absent
```

## Inputs (Facts)

| Name                | Description                                                                       | Default | Required |
| ------------------- | --------------------------------------------------------------------------------- | ------- | -------- |
| gcp_network         | The output from the module `google.cloud.gcp_compute_network`                     | null    | yes      |
| gcp_routers         | The output from the module `google.cloud.gcp_compute_router`                      | null    | yes      |
| gcp_attachments     | The output from the module `google.cloud.gcp_compute_attachments`                 | null    | yes      |
| pureport_network    | The output from the module `pureport.fabric.network`                                | null    | yes      |
| pureport_connection | The output from the module `pureport.fabric.google_cloud_interconnect_connection` | null    | yes      |

## Outputs (Registered Facts)

None
