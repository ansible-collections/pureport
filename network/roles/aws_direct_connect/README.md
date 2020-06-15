# Amazon Web Service Direct Connect Role

This role will declaritvely manage connections between Pureport's Multicloud
Fabric and Amazon Web Service using Direct Connect.

## Usage

This role can be used to either add a new connection (`state=present`) or 
remove an existing connection (`state=absent`).  By default, it will execute
with `state=present`.

- [Adding a connection to Amazon Web Service](docs/add_connection.md)
- [Removing a connection from Amazon Web Service](docs/remove_connection.md)

## Requirements

- Ansible 2.9 or later
- Pureport client 1.0.7 or later
- Boto
- Boto v3

### requirements.txt

```
ansible 
pureport-client
boto
boto3
```
