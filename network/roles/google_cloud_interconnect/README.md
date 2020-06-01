# Google Cloud Interconnect Role

Create connections between a Pureport Fabric cloud native network and Google
Cloud using high speed, Google Cloud Interconnect connections.

## Usage

This role can be used to either add a new connection (`state=present`) or 
remove an existing connection (`state=absent`).  By default, it will execute
with `state=present`.

- [Adding a connection to Google Cloud](docs/add_connection.md)
- [Removing a connection from Google Cloud](docs/remove_connection.md)

## Requirements

- Ansible 2.9 or later
- Pureport client 1.0.7 or later
- Google Auth 1.14.0 or later

### requirements.txt

```
ansible 
pureport-client
google-auth
```

