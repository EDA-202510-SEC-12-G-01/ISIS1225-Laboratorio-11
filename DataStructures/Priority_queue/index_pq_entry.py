def new_pq_entry(key, index):
    return {
        "key": key,
        "index": index,
    }

def set_key(my_entry, key):
    my_entry["key"] = key
    return my_entry

def set_index(my_entry, index):
    my_entry["index"] = index
    return my_entry

def get_key(my_entry):
    return my_entry["key"]

def get_index(my_entry):
    return my_entry["index"]