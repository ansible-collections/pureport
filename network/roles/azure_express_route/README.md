# Microsoft Azure ExpressRoute Role

This role will create and/or delete connections between a Pureport network and 
Microsoft Azure using ExpressRoute.  

## Usage

This role supports a stateful implementation for handling the adding or 
removing of Azure connections.  

This role can be used to either add a new connection (`state=present`) or 
remove an existing connection (`state=absent`).  By default, it will execute
with `state=present`.

- [Adding a connection to Microsoft Azure](docs/add_connection.md)
- [Removing a connection to Microsoft Azure](docs/remove_connection.md)

## Requirements

- Ansible 2.9 or later
- Pureport client 1.0.7 or later

### requirements.txt

```
ansible 
pureport-client
"ansible[azure]"
```

