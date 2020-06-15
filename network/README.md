# Pureport Ansible Network Collection

This collection provides a number of roles that can be used to automate the 
provisioning of Pureport cloud native networks as well as connections to public
cloud providers.

This collection supports:

  * Pureport networks and connections
  * Connecting Google Cloud to a Pureport Network
  * Connecting Amazon Web Service to a Pureport Network 
  * Connecting Microsoft Azure to a Pureport Network 

All connections are created as roles in this collection.  See the README file
in the cloud connection type of the roles directory for usage.

## Usage

This collection is designed for use with Ansible 2.9 or later.

## Roles

* `pureport.network.google_cloud_interconnect` - [README](roles/google_cloud_interconnect/README.md)
* `pureport.network.aws_direct_connect` - [README](roles/aws_direct_connect/README.md)
* `pureport.network.azure_express_route` - [README](roles/azure_express_route/README.md)

## Contributing

Please see [CONTRIBUTING](CONTRIBUTING.md) for details on contributing to this project

## License

Please see [LICENSE](LICENSE) for details
