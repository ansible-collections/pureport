# Copyright (c), Pureport, 2020
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


def get_state_argument_spec():
    """
    Return the basic state param
    :rtype: dict[str, dict]
    """
    return dict(
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )


def get_resolve_existing_argument_spec():
    """
    Return the basic resolve_existing param
    :rtype: dict[str, dict]
    """
    return dict(
        resolve_existing=dict(type='bool', default=True)
    )


def deep_compare(item, existing_item):
    """
    Given an item and an existing item, this recursively compares that all
    set keys/indexes in the item object are present in the existing item.
    :param * item:
    :param * existing_item:
    :returns: True if the objects are the same
    :rtype: bool
    """
    def compare(sub_item, sub_existing_item):
        # Compare dicts
        if isinstance(sub_item, dict) and isinstance(sub_existing_item, dict):
            for k in sub_item:
                try:
                    if compare(sub_item[k], sub_existing_item[k]) is False:
                        return False
                except KeyError:
                    # If the item has a key, but the existing one does not, check
                    # if the item's value is None
                    if compare(sub_item[k], None) is False:
                        return False
            return True
        # Compare lists
        if isinstance(sub_item, list) and isinstance(sub_existing_item, list):
            try:
                return all(compare(sub_item[i], sub_existing_item[i]) for i in range(len(sub_item)))
            except IndexError:
                # Lists were of different size
                return False
        # Compare the item to the existing item.  There's also a special case here
        # where the item may have been None, but the server returns a false boolean, empty list or empty dict.
        if sub_item == sub_existing_item:
            return True
        elif sub_item is None:
            return (isinstance(sub_existing_item, bool) and sub_existing_item is False) or \
                   (isinstance(sub_existing_item, dict) and len(sub_existing_item.items()) == 0) or \
                   (isinstance(sub_existing_item, list) and len(sub_existing_item) == 0)
        return False

    return compare(item, existing_item)


def item_crud(module,
              construct_item_fn,
              retrieve_existing_item_fn,
              resolve_existing_item_fn,
              create_item_fn,
              update_item_fn,
              delete_item_fn,
              compare_item_fn=deep_compare,
              copy_existing_item_properties_fn=lambda item, existing_item: item):
    """
    Handle a basic item's Ansible CRUD operations with state
    and changed functionality
    :param ansible.module_utils.basic.AnsibleModule module: the Ansible module
    :param () -> T construct_item_fn:
        A function that creates the item from the Ansible module params
    :param (T) -> T|None retrieve_existing_item_fn:
        A function that retrieves the existing item if applicable, otherwise None
    :param (T) -> T|None resolve_existing_item_fn:
        A function that resolves the existing item if applicable, otherwise None
    :param (T) -> T create_item_fn:
        A function that creates the item
    :param (T) -> T update_item_fn:
        A function that updates the existing item
    :param (T) -> T delete_item_fn:
        A function that updates the existing item
    :param (T, T) -> boolean compare_item_fn:
        A function that compares the Ansible item with the retrieved item.  Should
        return True if the items are the same.
    :param (T, T) -> T copy_existing_item_properties_fn:
        A function that copies existing properties from the retrieved item to the
        new item if the retrieved item exists.
    :rtype: (bool, T, T, T)
    """
    # Construct item object from the parameters
    item = construct_item_fn()

    # Retrieve the existing item if applicable
    existing_item = retrieve_existing_item_fn(item)
    if existing_item is None and module.params.get('resolve_existing'):
        existing_item = resolve_existing_item_fn(item)

    # Construct changed_item from existing properties
    changed_item = item
    if existing_item is not None:
        changed_item = copy_existing_item_properties_fn(item, existing_item)

    # Perform a simple comparison of the passed in item and existing item
    items_differ = not compare_item_fn(changed_item, existing_item)

    state = module.params.get('state')
    create_item = state == 'present' and existing_item is None
    update_item = state == 'present' and items_differ
    delete_item = state == 'absent' and existing_item is not None
    changed = create_item or update_item or delete_item

    if module.check_mode:
        module.exit_json(changed=changed)

    if create_item:
        changed_item = create_item_fn(changed_item)
    elif update_item:
        changed_item = update_item_fn(changed_item)
    elif delete_item:
        delete_item_fn(changed_item)
        changed_item = existing_item
    elif existing_item is not None:
        changed_item = existing_item

    return changed, changed_item, item, existing_item
