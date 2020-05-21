## pureport.aws

This Ansible Collection provides two modules that are required to automate the 
provisioning of AWS Direct Connect connections.  Both modules have been 
submitted to the Ansible AWS community collection and are currently under
community PR review.  

This collection provides a temporary home for the AWS modules until such time
as the Ansible AWS community completes their review of the pull requests.

IMPORTANT: This collection will, in all likelyhoood, just be a temporary home
for the modules until the Ansible AWS community review is complete.  

### Modules

This collection provides the following modules:

| Name                                | Description                                                                  |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| `direct_connect_virtual_interface ` | Fixes a bun in the origina module shipped with Ansible                       |
| `direct_connect_confirm_connection` | Finds DirectConnect connection and confirms it if it's in the ordering state |

### Ansible AWS Community

Both modules have been submitted to the Ansible AWS community for futher 
evaluation and consideration to be included in the Ansible AWS collection.  
Below are links to the sumbmitted PRs for reference.

| Name                                | PR Link                                                                  |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| `direct_connect_virtual_interface ` | [PR 52](https://github.com/ansible-collections/community.aws/pull/52)
| `direct_connect_confirm_connection` | [PR 53](https://github.com/ansible-collections/community.aws/pull/53)

Once the pull requests have been accepted, merged and released by the Ansible 
AWS community, this collection will be deprecated and ultimately removed from
Galaxy.

