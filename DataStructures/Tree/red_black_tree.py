from DataStructures.Tree import rbt_node as rbtn
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as ssl
from DataStructures.Map import map_separate_chaining as sc
from DataStructures.Map import map_linear_probing as lp

def default_compare(key, element):
    ek = rbtn.get_key(element)
    if key == ek:
        return 0
    return 1 if key > ek else -1

def new_map():
    return {'root': None, 'type': 'RBT'}

def put(my_rbt, key, value):
    my_rbt['root'] = insert_node(my_rbt['root'], key, value)
    rbtn.change_color(my_rbt['root'], rbtn.BLACK)
    return my_rbt

def insert_node(root, key, value):
    if root is None:
        return rbtn.new_node(key, value)
    cmp = default_compare(key, root)
    if cmp < 0:
        root['left'] = insert_node(root['left'], key, value)
    elif cmp > 0:
        root['right'] = insert_node(root['right'], key, value)
    else:
        root['value'] = value
    return balance(root)


def get(my_rbt, key):
    return get_node(my_rbt['root'], key)


def get_node(root, key):
    if root is None:
        return None
    cmp = default_compare(key, root)
    if cmp < 0:
        return get_node(root['left'], key)
    elif cmp > 0:
        return get_node(root['right'], key)
    else:
        return rbtn.get_value(root)


def remove(my_rbt, key):
    if not contains(my_rbt, key):
        return my_rbt
    my_rbt['root'] = remove_node(my_rbt['root'], key)
    if my_rbt['root']:
        rbtn.change_color(my_rbt['root'], rbtn.BLACK)
    return my_rbt

def remove_node(h, key):
    if default_compare(key, h) < 0:
        if not rbtn.is_red(h['left']) and not rbtn.is_red(h['left']['left']):
            h = move_red_left(h)
        h['left'] = remove_node(h['left'], key)
    else:
        if rbtn.is_red(h['left']):
            h = rotate_right(h)
        if default_compare(key, h) == 0 and h['right'] is None:
            return None
        if not rbtn.is_red(h['right']) and not rbtn.is_red(h['right']['left']):
            h = move_red_right(h)
        if default_compare(key, h) == 0:
            succ = get_min_node(h['right'])
            h['key'], h['value'] = succ['key'], succ['value']
            h['right'] = delete_min_node(h['right'])
        else:
            h['right'] = remove_node(h['right'], key)
    return balance(h)


def contains(my_rbt, key):
    return get(my_rbt, key) is not None

def size(my_rbt):
    return size_tree(my_rbt['root'])


def is_empty(my_rbt):
    return my_rbt['root'] is None

def key_set(my_rbt):
    lst = ssl.new_list()
    return key_set_tree(my_rbt['root'], lst)

def key_set_tree(root, key_list):
    if root is None:
        return key_list
    key_set_tree(root['left'], key_list)
    ssl.add_last(key_list, rbtn.get_key(root))
    key_set_tree(root['right'], key_list)
    return key_list

def value_set(my_rbt):
    lst = ssl.new_list()
    return value_set_tree(my_rbt['root'], lst)

def value_set_tree(root, value_list):
    if root is None:
        return value_list
    value_set_tree(root['left'], value_list)
    ssl.add_last(value_list, rbtn.get_value(root))
    value_set_tree(root['right'], value_list)
    return value_list

def get_min(my_rbt):
    node = get_min_node(my_rbt['root'])
    return rbtn.get_key(node) if node else None

def get_min_node(root):
    if root is None:
        return None
    while root['left']:
        root = root['left']
    return root

def get_max(my_rbt):
    node = get_max_node(my_rbt['root'])
    return rbtn.get_key(node) if node else None

def get_max_node(root):
    if root is None:
        return None
    while root['right']:
        root = root['right']
    return root

def delete_min(my_rbt):
    if my_rbt['root'] is None:
        return my_rbt
    my_rbt['root'] = delete_min_node(my_rbt['root'])
    if my_rbt['root']:
        rbtn.change_color(my_rbt['root'], rbtn.BLACK)
    return my_rbt

def delete_max(my_rbt):
    if my_rbt['root'] is None:
        return my_rbt
    my_rbt['root'] = delete_max_node(my_rbt['root'])
    if my_rbt['root']:
        rbtn.change_color(my_rbt['root'], rbtn.BLACK)
    return my_rbt

def delete_max_node(root):
    if rbtn.is_red(root['left']):
        root = rotate_right(root)
    if root['right'] is None:
        return None
    if not rbtn.is_red(root['right']) and not rbtn.is_red(root['right']['left']):
        root = move_red_right(root)
    root['right'] = delete_max_node(root['right'])
    return balance(root)

def floor(my_rbt, key):
    node = floor_key(my_rbt['root'], key)
    return rbtn.get_key(node) if node else None

def floor_key(root, key):
    if not root:
        return None
    cmp = default_compare(key, root)
    if cmp == 0:
        return root
    if cmp < 0:
        return floor_key(root['left'], key)
    t = floor_key(root['right'], key)
    return t if t else root

def ceiling(my_rbt, key):
    node = ceiling_key(my_rbt['root'], key)
    return rbtn.get_key(node) if node else None

def ceiling_key(root, key):
    if not root:
        return None
    cmp = default_compare(key, root)
    if cmp == 0:
        return root
    if cmp > 0:
        return ceiling_key(root['right'], key)
    t = ceiling_key(root['left'], key)
    return t if t else root

def select(my_rbt, pos):
    node = select_key(my_rbt['root'], pos)
    return rbtn.get_key(node) if node else None

def select_key(root, pos):
    if not root:
        return None
    left_size = size_tree(root['left'])
    if left_size > pos:
        return select_key(root['left'], pos)
    if left_size < pos:
        return select_key(root['right'], pos - left_size - 1)
    return root

def rank(my_rbt, key):
    return rank_keys(my_rbt['root'], key)

def rank_keys(root, key):
    if not root:
        return 0
    cmp = default_compare(key, root)
    if cmp < 0:
        return rank_keys(root['left'], key)
    elif cmp > 0:
        return 1 + size_tree(root['left']) + rank_keys(root['right'], key)
    else:
        return size_tree(root['left'])

def height(my_rbt):
    return height_tree(my_rbt['root'])

def height_tree(root):
    if not root:
        return 0
    return 1 + max(height_tree(root['left']), height_tree(root['right']))

def keys(my_rbt, key_initial, key_final):
    lst = ssl.new_list()
    keys_range(my_rbt['root'], key_initial, key_final, lst)
    return lst

def values(my_rbt, key_initial, key_final):
    lst = ssl.new_list()
    values_range(my_rbt['root'], key_initial, key_final, lst)
    return lst

def values_range(root, key_initial, key_final, value_list):
    if not root:
        return
    if default_compare(key_initial, root) < 0:
        values_range(root['left'], key_initial, key_final, value_list)
    if default_compare(key_initial, root) <= 0 and default_compare(key_final, root) >= 0:
        ssl.add_last(value_list, rbtn.get_value(root))
    if default_compare(key_final, root) > 0:
        values_range(root['right'], key_initial, key_final, value_list)

def rotate_left(h):
    x = h['right']
    h['right'] = x['left']
    x['left'] = h
    x['color'] = h['color']
    rbtn.change_color(h, rbtn.RED)
    return x

def rotate_right(h):
    x = h['left']
    h['left'] = x['right']
    x['right'] = h
    x['color'] = h['color']
    rbtn.change_color(h, rbtn.RED)
    return x

def flip_node_color(h):
    rbtn.change_color(h, rbtn.RED if h['color']==rbtn.BLACK else rbtn.BLACK)
    return h

def flip_colors(h):
    flip_node_color(h)
    flip_node_color(h['left'])
    flip_node_color(h['right'])
    return h

def size_tree(root):
    if root is None:
        return 0
    return 1 + size_tree(root['left']) + size_tree(root['right'])

def keys_range(root, key_initial, key_final, list_key):
    if not root:
        return
    if default_compare(key_initial, root) < 0:
        keys_range(root['left'], key_initial, key_final, list_key)
    if default_compare(key_initial, root) <= 0 and default_compare(key_final, root) >= 0:
        ssl.add_last(list_key, rbtn.get_key(root))
    if default_compare(key_final, root) > 0:
        keys_range(root['right'], key_initial, key_final, list_key)

def delete_min_node(h):
    if h['left'] is None:
        return None
    if not rbtn.is_red(h['left']) and not rbtn.is_red(h['left']['left']):
        h = move_red_left(h)
    h['left'] = delete_min_node(h['left'])
    return balance(h)

def move_red_right(h):
    flip_colors(h)
    if rbtn.is_red(h['left']['left']):
        h = rotate_right(h)
        flip_colors(h)
    return h

def move_red_left(h):
    flip_colors(h)
    if rbtn.is_red(h['right']['left']):
        h['right'] = rotate_right(h['right'])
        h = rotate_left(h)
        flip_colors(h)
    return h

def balance(h):
    if rbtn.is_red(h['right']):
        h = rotate_left(h)
    if rbtn.is_red(h['left']) and rbtn.is_red(h['left']['left']):
        h = rotate_right(h)
    if rbtn.is_red(h['left']) and rbtn.is_red(h['right']):
        flip_colors(h)
    return h

def left_key(my_rbt):
    return get_min(my_rbt)


def right_key(my_rbt):
    return get_max(my_rbt)