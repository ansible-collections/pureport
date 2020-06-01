# Adding a connection to Google Cloud

When setting the `state` value to `present` (default), a new connection will
be added between Pureport and Google Cloud, if the connection does not already
exist.  

## Example

```yaml
---
- hosts: localhost

  roles:
    - name: pureport.network.google_cloud_interconnect
      gcp_region: us-central1
      gcp_network_name: default
      gcp_router_name: router
      gcp_interconnect_name: vlan
      pureport_network_name: default
      pureport_connection_name: gcp
      pureport_connection_speed: 50
      state: present
```

## Inputs (Facts)

| Name                     | Description                                                        | Default | Required |
| ------------------------ | ------------------------------------------------------------------ | ------- | -------- |
| gcp_region               | The Google Cloud region where the connection should be built       | null    | yes      |
| gcp_network_name         | The name of the Google Cloud VPC to associate with this connection | vpc     | no       |
| gcp_router_name          | The name of the Google Cloud router to be created                  | router  | no       |
| gcp_interconnect_name    | The name of the Google Cloud connection to be created              | vlan    | no       |
| pureport_network_name    | The name of the Pureport network to attach to this connection      | default | no       |
| pureport_connection_name | The name of the Pureport connection to be created                  | gateway | no       |

## Outputs (Registered Facts)

| Name                | Description                                                       |
| ------------------- | ----------------------------------------------------------------- |
| gcp_network         | The output from the module `google.cloud.gcp_compute_network'     |
| gcp_routers         | The output from the module `google.cloud.gcp_compute_router`      |
| gcp_attachments     | The output from the module `google.cloud.gcp_compute_attachments` |
| pureport_network    | The output from the module `pureport.fabric.network`              |
| pureport_connection | The output from the module `pureport.fabric.google_cloud_interconnect_connection`           |

