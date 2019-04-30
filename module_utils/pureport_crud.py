

def deep_compare(item, existing_item):
    """
    Compares that all key-value pairs or array items in an item match what's in the existing_item
    :param * item:
    :param * existing_item:
    :rtype: bool
    """
    def compare(sub_item, sub_existing_item):
        if isinstance(sub_item, dict) and isinstance(sub_existing_item, dict):
            return all(compare(sub_item[k], sub_existing_item[k]) for k in sub_item)
        if isinstance(sub_item, list) and isinstance(sub_existing_item, list):
            return all(compare(sub_item[i], sub_existing_item[i]) for i in range(len(sub_item)))
        return sub_item == sub_existing_item

    return compare(item, existing_item)


def item_crud(module,
              construct_item_fn,
              retrieve_existing_item_fn,
              create_item_fn,
              update_item_fn,
              delete_item_fn,
              compare_item_fn=deep_compare):
    """
    Handle a basic item's Ansible CRUD operations with state
    and changed functionality
    :param AnsibleModule module: the Ansible module
    :param () -> T construct_item_fn:
        A function that creates the item from the Ansible module params
    :param (T) -> T|None retrieve_existing_item_fn:
        A function that retrieves the existing item if applicable, otherwise None
    :param (T) -> T create_item_fn:
        A function that creates the item
    :param (T, T) -> T update_item_fn:
        A function that updates the existing item
    :param (T, T) -> T delete_item_fn:
        A function that updates the existing item
    :param (T, T) -> boolean compare_item_fn:
        A function that compares the Ansible item with the retrieved item
    :rtype: (bool, T, T, T)
    """
    # Construct item object from the parameters
    item = construct_item_fn()

    # Retrieve the existing item if applicable
    existing_item = retrieve_existing_item_fn(item)

    # Perform a simple comparison of the passed in network and existing network
    items_differ = compare_item_fn(item, existing_item)

    state = module.params['state']
    changed = (state == 'present' and items_differ) or \
              (state == 'absent' and existing_item is None)

    updated_item = item
    if state == 'present':
        # Create item
        if existing_item is None:
            updated_item = create_item_fn(item)
        # Update item
        elif items_differ:
            updated_item = update_item_fn(item, existing_item)
    # Delete Network
    elif state == 'absent' and existing_item is not None:
        delete_item_fn(item, existing_item)
        updated_item = existing_item

    return changed, updated_item, item, existing_item
