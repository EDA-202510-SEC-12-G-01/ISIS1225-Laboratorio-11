from DataStructures.List.list_node import new_single_node
from DataStructures.List.list_node import get_element as get_node_info

def new_list():
    return {
        'size': 0,
        'first': None,
        'last': None,
        'type': 'single_linked_list'
    }

def is_empty(my_list):
    return my_list['size'] == 0

def size(my_list):
    return my_list['size']

def add_first(my_list, element):
    new_node = new_single_node(element)
    if my_list['size'] == 0:
        my_list['first'] = new_node
        my_list['last'] = new_node
    else:
        new_node['next'] = my_list['first']
        my_list['first'] = new_node
    my_list['size'] += 1
    return my_list

def add_last(my_list, element):
    new_node = new_single_node(element)
    if my_list['size'] == 0:
        my_list['first'] = new_node
        my_list['last'] = new_node
    else:
        my_list['last']['next'] = new_node
        my_list['last'] = new_node
    my_list['size'] += 1
    return my_list

def first_element(my_list):
    if my_list['size'] == 0:
        raise IndexError("list index out of range")
    return get_node_info(my_list['first'])

def last_element(my_list):
    if my_list['size'] == 0:
        raise IndexError("list index out of range")
    return get_node_info(my_list['last'])

def get_element(my_list, pos):
    if pos < 0 or pos >= my_list['size']:
        raise IndexError("list index out of range")
    current = my_list['first']
    for _ in range(pos):
        current = current['next']    
    return get_node_info(current)

def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list['size']:
        raise IndexError("list index out of range")
    if pos == 0:
        first_node = my_list['first']
        my_list['first'] = first_node['next']
        if my_list['size'] == 1:
            my_list['last'] = None
    else:
        previous = my_list['first']
        for _ in range(pos - 1):
            previous = previous['next']
        node_to_delete = previous['next']
        previous['next'] = node_to_delete['next']
        if node_to_delete == my_list['last']:
            my_list['last'] = previous
    my_list['size'] -= 1
    return my_list

def remove_first(my_list):
    if my_list['size'] == 0:
        raise IndexError("list index out of range")
    node_to_remove = my_list['first']
    info_removed = get_node_info(node_to_remove)
    my_list['first'] = node_to_remove['next']
    my_list['size'] -= 1
    if my_list['size'] == 0:
        my_list['last'] = None
    return info_removed

def remove_last(my_list):
    if my_list['size'] == 0:
        raise IndexError("list index out of range")
    if my_list['size'] == 1:
        info_removed = get_node_info(my_list['first'])
        my_list['first'] = None
        my_list['last'] = None
        my_list['size'] = 0
        return info_removed
    current = my_list['first']
    while current['next'] != my_list['last']:
        current = current['next']
    info_removed = get_node_info(my_list['last'])
    current['next'] = None
    my_list['last'] = current
    my_list['size'] -= 1
    return info_removed

def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list['size']:
        raise IndexError("list index out of range")
    new_node = new_single_node(element)
    if pos == 0:
        new_node['next'] = my_list['first']
        my_list['first'] = new_node
        if my_list['size'] == 0:
            my_list['last'] = new_node
    elif pos == my_list['size']:
        my_list['last']['next'] = new_node
        my_list['last'] = new_node
    else:
        current = my_list['first']
        for _ in range(pos - 1):
            current = current['next']
        new_node['next'] = current['next']
        current['next'] = new_node
    my_list['size'] += 1
    return my_list

def default_function(element_1, element_2):
    if element_1 > element_2:
        return 1
    elif element_1 < element_2:
        return -1
    else:
        return 0

def is_present(my_list, element, cmp_function):
    current = my_list['first']
    pos = 0
    while current is not None:
        current_info = get_node_info(current)
        if cmp_function(current_info, element) == 0:
            return pos
        current = current['next']
        pos += 1
    return -1

def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list['size']:
        raise IndexError("list index out of range")
    current = my_list['first']
    for _ in range(pos):
        current = current['next']
    current['info'] = new_info
    return my_list

def exchange(my_list, pos_1, pos_2):
    size = my_list['size']
    if pos_1 < 0 or pos_1 >= size or pos_2 < 0 or pos_2 >= size:
        raise IndexError("list index out of range")
    if pos_1 == pos_2:
        return my_list
    if pos_1 > pos_2:
        pos_1, pos_2 = pos_2, pos_1
    current = my_list['first']
    node_1 = None
    node_2 = None
    for i in range(pos_2 + 1):
        if i == pos_1:
            node_1 = current
        if i == pos_2:
            node_2 = current
        current = current['next']
    info_1 = get_node_info(node_1)
    info_2 = get_node_info(node_2)
    node_1['info'] = info_2
    node_2['info'] = info_1
    return my_list

def sub_list(my_list, pos, num_elements):
    if pos < 0 or pos >= my_list['size']:
        raise IndexError("list index out of range")
    if pos + num_elements > my_list['size']:
        raise IndexError("list index out of range")
    new_sublist = new_list()
    current = my_list['first']
    for _ in range(pos):
        current = current['next']
    for _ in range(num_elements):
        info = get_node_info(current)
        add_last(new_sublist, info)
        current = current['next']
    return new_sublist

def default_sort_criteria(element_1, element_2):
   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted

def selection_sort(lst, sort_crit):
    n = size(lst)
    for i in range(n - 1):
        minimum = i
        for j in range(i + 1, n):
            if sort_crit(get_element(lst, j), get_element(lst, minimum)):
                minimum = j
        exchange(lst, i, minimum)
    return lst

def insertion_sort(lst, sort_crit):
    n = size(lst)
    for i in range(1, n):
        j = i
        while j > 0 and sort_crit(get_element(lst, j), get_element(lst, j-1)):
            exchange(lst, j, j-1)
            j -= 1
    return lst

def shell_sort(lst, sort_crit):
    n = size(lst)
    h = 1
    while h < n/3:
        h = 3 * h + 1
    while h >= 1:
        for i in range(h, n):
            j = i
            while j >= h and sort_crit(get_element(lst, j), get_element(lst, j - h)):
                exchange(lst, j, j - h)
                j -= h
        h //= 3
    return lst

def merge_sort(lst, sort_crit):
    n = size(lst)
    if n > 1:
        mid = n // 2
        left_list = sub_list(lst, 0, mid)
        right_list = sub_list(lst, mid, n - mid)
        merge_sort(left_list, sort_crit)
        merge_sort(right_list, sort_crit)
        i = j = k = 0
        left_size = size(left_list)
        right_size = size(right_list)
        while i < left_size and j < right_size:
            if sort_crit(get_element(right_list, j), get_element(left_list, i)):
                change_info(lst, k, get_element(right_list, j))
                j += 1
            else:
                change_info(lst, k, get_element(left_list, i))
                i += 1
            k += 1
        while i < left_size:
            change_info(lst, k, get_element(left_list, i))
            i += 1
            k += 1
        while j < right_size:
            change_info(lst, k, get_element(right_list, j))
            j += 1
            k += 1
    return lst

def quick_sort(lst, sort_crit):
    def partition(lo, hi):
        follower = lo
        pivot = get_element(lst, hi)
        for leader in range(lo, hi):
            if sort_crit(get_element(lst, leader), pivot):
                exchange(lst, follower, leader)
                follower += 1
        exchange(lst, follower, hi)
        return follower
    def quicksort(lo, hi):
        if lo < hi:
            pivot_index = partition(lo, hi)
            quicksort(lo, pivot_index - 1)
            quicksort(pivot_index + 1, hi)
    n = size(lst)
    if n > 0:
        quicksort(0, n - 1)
    return lst