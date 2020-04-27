
1.0.0 / 2020-04-27
==================

  * Moves test/ directory to tests/
  * Correcting imports for ansible sanity tests
  * Add scripts for testing the collection
  * Removes 3rd party modules
  * Move the fabric collection into its own subdirectory

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
