
1.0.0 / 2020-05-17
==================

  * Removes all older `pureport_*` modules in favor of the newer module names.
     * **Note**: See the table below for a migration reference.
  * Moves test/ directory to tests/
  * Correcting imports for ansible sanity tests
  * Add scripts for testing the collection
  * Removes 3rd party modules
    * [`pureport.fabric.aws_direct_connect_confirm_connection -> `community.aws.aws_direct_connect_confirm_connection`](https://github.com/ansible-collections/community.aws/pull/53)
    * [`pureport.fabric.pr_48711_aws_direct_connect_virtual_interface -> `community.aws.aws_direct_connect_virtual_interface`](https://github.com/ansible-collections/community.aws/pull/53)
  * Move the fabric collection into its own subdirectory

| Pureport 1.X Name                     | Pureport 0.X Name                              |
|---------------------------------------|------------------------------------------------|
|`access_token_info`                    |`pureport_access_token_fact`                    |
|`locations_info`                       |`pureport_location_facts`                       |
|`facilities_info`                      |`pureport_facility_facts`                       |
|`options_info`                         |`pureport_option_facts`                         |
|`cloud_regions_info`                   |`pureport_cloud_region_facts`                   |
|`cloud_services_info`                  |`pureport_cloud_service_facts`                  |
|`accounts_info`                        |`pureport_account_facts`                        |
|`supported_connections_info`           |`pureport_supported_connection_facts`           |
|`supported_ports_info`                 |`pureport_supported_port_facts`                 |
|`ports_info`                           |`pureport_port_facts`                           |
|`port`                                 |`pureport_port`                                 |
|`networks_info`                        |`pureport_network_facts`                        |
|`network`                              |`pureport_network`                              |
|`connections_info`                     |`pureport_connection_facts`                     |
|`aws_direct_connect_connection`        |`pureport_aws_direct_connect_connection`        |
|`azure_express_route_connection`       |`pureport_azure_express_route_connection`       |
|`google_cloud_interconnect_connection` |`pureport_google_cloud_interconnect_connection` |
|`port_connection`                      |`pureport_port_connection`                      |
|`site_ipsec_vpn_connection`            |`pureport_site_ipsec_vpn_connection`            |

0.12.0 / 2020-04-21
===================

  * Update site connection IKE/ESP config options
  * Add tags for all connections and network
  * Default connections billing term to 'HOURLY'
  * Removes all examples and updates the README
  * Removes roles from the official collection
  * Use id or href to handle links

0.11.0 / 2020-04-10
===================

  * Update README about Python dependencies

0.10.0 / 2020-04-10
===================

  * Upgrade pureport-client to 1.0.4
  * adds check mode support to info modules
  * Add codeowners
  * updates all code files with appropriate license headers
  * refactors pureport.py module
  * renames the collection to pureport.fabric
  * Correct lint warnings in workflow
  * Use github action instead of on-prem Jenkins
  * Update repository location

0.0.9 / 2020-03-10
==================

  * Correct galaxy.yml indentation
  * Add build_ignore for ansible collection 2.10
  * Rename all modules
  * Update README and CONTRIBUTING docs
  * Use relative imports for modules/module_utils
  * Remove PR GCP Compute Interconnect Attachment module
  * Correct null pointer with 'api_base_url' module parameter

0.0.8 / 2019-08-20
==================

  * Add optional AWS Internet Gateway to pureport_aws role

0.0.7 / 2019-07-26
==================

  * Correct documentation

0.0.6 / 2019-07-26
==================

  * Correct namespace name and fix mazer build
  * Correct ansible-doc documentation for modules
  * Rework examples to use new roles
  * Switch to Ansible Collections structure
  * Add a hybrid example with two AWS, one GC and a VPN connection

0.0.5 / 2019-06-13
==================

  * Remove cases where we infer the link object id
  * Add facilities, supported ports, and ports

0.0.4 / 2019-05-15
==================

  * Correct test cases for AWS
  * Set virtualenv python path to 'python' instead of the relative path
  * Move ansible package to the top level directory, rename 'modules' to 'library'

0.0.3 / 2019-05-14
==================

  * Add more tags and cloud platforms to galaxy.yml

0.0.2 / 2019-05-14
==================

  * Update galaxy tags and platforms in galaxy.yml
  * Correct some issues with README documentation
  * Correct module example documentation

0.0.1 / 2019-05-13
==================

  * Update Azure example
  * Remove network/connection id from examples
  * Clean up AWS Direct Connect example
  * Return existing item if no changes
  * Return all variables as snake_case
  * Return the connection/network objects exploded into the module result
  * Add VPC Subnet and VPC Route Table to aws example
  * Add AWS example
  * Add tests for update/deletes using name
  * Correct issue with existing id not being copied before compare
  * Add resolution of networks/connections by name
  * Clean up some documentation of return values
  * Simplify Google example
  * Add initial azure express route example
  * Add cloud_region_facts
  * Add sub-options to some list/dict params
  * Add initial example of creating a GCI connection
  * Don't log the access token
  * Ensure that users reuse the obtained access token across tasks
  * Adding modules for other facts that may be required for creating connections
  * Adding a trick to not install files with Ansible Galaxy
  * Add examples to each module
  * Create LICENSE
  * Switch to using href's everywhere instead of link objects
  * Split out nat configurations
  * Add site ipsec vpn connection
  * Add azure express route module
  * Move modules into the ansible package to correct development imports
  * Adding network and connection creation
