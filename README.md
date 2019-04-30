Structure of project similar to
https://github.com/Apstra/aos-ansible/tree/migrate-rest-api

https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#developing-locally
https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_checklist.html
https://docs.ansible.com/ansible/devel/dev_guide/developing_module_utilities.html

> However, contributing to the main project isn't the only way to distribute a module - 
you can embed modules in roles on Galaxy or simply share copies of your module code for local use.


https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#adding-a-module-locally
https://docs.ansible.com/ansible/latest/reference_appendices/config.html?highlight=module_utils#envvar-ANSIBLE_MODULE_UTILS
> any directory added to the `ANSIBLE_LIBRARY` environment variable (`$ANSIBLE_LIBRARY` takes a colon-separated list like `$PATH`)
> any directory added to the `ANSIBLE_MODULE_UTILS` environment variable (`$ANSIBLE_MODULE_UTILS` takes a colon-separated list like `$PATH`)

Relevant links:
https://stackoverflow.com/questions/44786473/how-to-get-ansible-module-utils-to-resolve-my-custom-directory/44790883#44790883
