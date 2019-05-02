## Description
This is a collection of Ansible [library modules](https://docs.ansible.com/ansible/2.8/user_guide/modules_intro.html) which can
interact with the [Pureport](https://www.pureport.com/) ReST API.

It provides the following modules you can use in your own roles:
- `pureport_network_facts` - used to list a set of networks
- `pureport_network` - used to create/update/delete a network
- `pureport_connection_facts` - used to list a set of connections
- `pureport_aws_direct_connect_connection` - used to create/update/delete a Pureport AWS connection

## Installation
This "role" is distributed via [ansible-galaxy](https://galaxy.ansible.com/) (bundled with Ansible).

```bash
ansible-galaxy install pureport-ansible-modules
```

Because this is not a collection of "roles" and is instead intended to be used within your own roles, you'll need to tell
Ansible where to find these modules and their utilities.

This can be done via Environment variables ([1](https://docs.ansible.com/ansible/2.8/dev_guide/developing_locally.html#adding-a-module-locally),
[1.1](https://docs.ansible.com/ansible/2.8/reference_appendices/config.html#envvar-ANSIBLE_LIBRARY),
[2](https://docs.ansible.com/ansible/2.8/reference_appendices/config.html?highlight=module_utils#envvar-ANSIBLE_MODULE_UTILS)):

```bash
PROJECT_DIRECTORY="YOUR PROJECT DIRECTORY HERE"
PUREPORT_ANSIBLE_MODULES_DIR=${PROJECT_DIRECTORY}/roles.galaxy/pureport-ansible-modules
export ANSIBLE_LIBRARY=${PUREPORT_ANSIBLE_MODULES_DIR}/modules
export ANSIBLE_MODULE_UTILS=${PUREPORT_ANSIBLE_MODULES_DIR}/module_utils
```

It can also be done via `ansible.cfg` file ([1](https://docs.ansible.com/ansible/2.8/reference_appendices/config.html#default-module-path),
[2](https://docs.ansible.com/ansible/2.8/reference_appendices/config.html#default-module-utils-path)):
```ini
library = roles.galaxy/pureport-ansible-modules/modules
module_utils = roles.galaxy/pureport-ansible-modules/module_utils
```

## Module Documentation
**NOTE**: This will only work with Ansible 2.8 (via this [PR](https://github.com/ansible/ansible/pull/50172)) which opens up
the `ANSIBLE_DOC_FRAGMENT_PLUGINS` environment variable for shared documentation in modules.

Because the modules for this are external to Ansible and some of the documentation is shared via 
[doc_fragments](https://docs.ansible.com/ansible/2.8/dev_guide/developing_modules_documenting.html#documentation-fragments), for 
documentation to work with the `ansible-doc`, simply do the following:
```bash
PROJECT_DIRECTORY="YOUR PROJECT DIRECTORY HERE"
PUREPORT_ANSIBLE_MODULES_DIR=${PROJECT_DIRECTORY}/roles.galaxy/pureport-ansible-modules
export ANSIBLE_DOC_FRAGMENT_PLUGINS=${PUREPORT_ANSIBLE_MODULES_DIR}/plugins/doc_fragments
```

It can also be done via `ansible.cfg` file ([1](https://docs.ansible.com/ansible/2.8/reference_appendices/config.html#doc-fragment-plugin-path))
```yaml
doc_fragment_plugins = roles.galaxy/pureport-ansible-modules/plugins/doc_fragments
```

You can then 
```bash
ansible-docs pureport_network_facts
ansible-docs pureport_network
ansible-docs pureport_connection_facts
ansible-docs pureport_aws_direct_connect_connection
```

## Development
This project uses:
- [tox](https://tox.readthedocs.io/en/latest/) - A generic virtualenv management and test command line tool
- [pytest](https://docs.pytest.org/en/latest/) - A Python testing framework
- [flake8](http://flake8.pycqa.org/en/latest/) - A Python lint tool
- [yamllint](https://yamllint.readthedocs.io/en/stable/) - A YAML lint tool

To build from scratch, first install `tox`.

```bash
pip install tox
```

Then run tox from the root directory.

```bash
tox
```

### Writing a Module
We should follow these guidelines for writing/maintaining Modules:
- Follow the documentation on [writing your own module](https://docs.ansible.com/ansible/2.8/dev_guide/developing_locally.html).
- Follow the documentation on the [module checklist](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_checklist.html).
- Write good documentation for the module [using this as a guide](https://docs.ansible.com/ansible/2.8/dev_guide/developing_modules_documenting.html).

#### Writing a shared Module Utility
[Module utilities](https://docs.ansible.com/ansible/latest/dev_guide/developing_module_utilities.html) are a great way to share 
code between modules.  They should be located in the `module_utils/pureport` package.

When importing a `module_util` into a module, use an `ansible` prefixed path to import it.

```python
# like this
import ansible.module_utils.pureport.pureport

# or like this
from ansible.module_utils.pureport.pureport import get_client
```

#### Writing shared Documentation
Ansible supports a documentation feature called 
[`extends_documentation_fragment`](https://docs.ansible.com/ansible/2.8/dev_guide/developing_modules_documenting.html#documentation-fragments), 
which basically merges the documentation of a module and a fragment or list of fragments.

A documentation fragment should live in the `plugins/doc_fragments` directory.  The documentation fragment module should be a file 
with a single class called `ModuleDocFragment` and it should contain a variable called `DOCUMENTATION`.

For example:

*plugins/doc_fragments/pureport_my_parameter.py*
```python
class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    my_parameter:
        description:
            - A simple shared parameter
        required: false
        type: bool
    '''
```

You can then use the documentation fragment in a module, referencing it via module name:
```python
DOCUMENTATION = '''
---
...

extends_documentation_fragment:
    - pureport_my_parameter
'''
```

##### Documentation Errors
I encountered one or two errors while writing documentation.  If you see the following, it's likely because of a formatting error
with an `options` description field.
```bash
ansible-doc pureport_network_facts
ERROR! module pureport_network_facts has a documentation error formatting or is missing documentation.
```

Description fields should use a line continuation with prefixed with `- `, like so:
```yaml
options:
    my_parameter:
        description:
            - A simple shared parameter that does X, Y, Z.  This is
            - required if you need A, B, C.  # The continuation here starts with `- `
        required: false
        type: bool
```


### Testing a Module
There are two ways to test a module, either run a Playbook with it or write a PyTest script.  A Playbook is likely easier, but
PyTest's allow you to mock and act as unit tests.

#### Writing a Playbook
The `test/playbooks` directory contains a set of playbook tests which interact with our modules.  Feel free to write your own
and attach them to the `main.yml` playbook.  There is also a secondary [README.md](test/playbooks/README.md) which discusses
setup, such as configuring defaults with `group_vars`.

To run those, you will need to perform the directions mentioned in the [Installation](#Installation) section, but
instead of installing with ansible-galaxy, just point all environment variables to the local paths.

```bash
PUREPORT_ANSIBLE_MODULES_DIR="THE PROJECT DIRECTORY HERE"
export ANSIBLE_LIBRARY=${PUREPORT_ANSIBLE_MODULES_DIR}/modules
export ANSIBLE_MODULE_UTILS=${PUREPORT_ANSIBLE_MODULES_DIR}/module_utils
export ANSIBLE_DOC_FRAGMENT_PLUGINS=${PUREPORT_ANSIBLE_MODULES_DIR}/plugins/doc_fragments
```

#### Writing a PyTest
Coming soon!

