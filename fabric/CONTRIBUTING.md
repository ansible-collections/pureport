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
Follow these guidelines for writing/maintaining Modules:
- Follow the documentation on [writing your own module](https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html).
- Follow the documentation on the [module checklist](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_checklist.html).
- Write good documentation for the module [using this as a guide](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html).

All modules should live in the `plugins/modules` package.  All modules should be prefixed with `pureport_`.

#### Writing a shared Module Utility
[Module utilities](https://docs.ansible.com/ansible/latest/dev_guide/developing_module_utilities.html) are a great way to share 
code between modules.  They should be located in the `plugins/module_utils` package. 

When importing a `module_util` use the relative path as shown below.


```python
# like this
import ..module_utils.pureport_client

# or like this
from ..module_utils.pureport_client import get_client
```

#### Writing shared Documentation
Ansible supports a documentation feature called 
[`extends_documentation_fragment`](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#documentation-fragments), 
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
    - pureport.fabric.pureport_my_parameter
'''
```

##### Documentation Errors
I encountered one or two errors while writing documentation.  If you see the following, it's likely because of a formatting error
with an `options` description field.
```bash
ansible-doc pureport.fabric.pureport_network_facts
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

#### Writing a Test Playbook
The `test/playbooks` directory contains a set of playbook tests which interact with our modules.  Feel free to write your own
and attach them to the `main.yml` playbook.  There is also a secondary [README.md](test/playbooks/README.md) which discusses
setup, such as configuring defaults with `group_vars`.

#### Writing a PyTest
Coming soon!

