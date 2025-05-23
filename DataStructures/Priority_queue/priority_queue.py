from DataStructures.List import array_list as lt
from DataStructures.Priority_queue import index_pq_entry as pqe

def default_compare_lower_value(father_node, child_node):
    if pqe.get_key(father_node) <= pqe.get_key(child_node):
        return True
    return False

def default_compare_higher_value(father_node, child_node):
    if pqe.get_key(father_node) >= pqe.get_key(child_node):
        return True
    return False

def new_heap(is_min_pq=True):
    heap = {
        'elements': lt.new_list(),
        'size': 0,
        'cmp_function': default_compare_lower_value if is_min_pq else default_compare_higher_value
        }
    return heap

def size(my_heap):
    return my_heap['size']

def is_empty(my_heap):
    return my_heap['size'] == 0

def priority(my_heap, parent, child):
    cmp = my_heap["cmp_function"](parent, child)
    if cmp > 0:
        return True
    return False

def swim(my_heap, pos):
    while pos > 1:
        parent_pos = pos // 2
        parent = lt.get_element(my_heap["elements"], parent_pos - 1)
        child  = lt.get_element(my_heap["elements"], pos - 1)
        if child['key'] < parent['key']:
            lt.exchange(my_heap["elements"], pos - 1, parent_pos - 1)
            pos = parent_pos
        else:
            break
    return my_heap

def sink(my_heap, pos):
    elements = my_heap['elements']['elements']
    size = my_heap['size']
    while 2 * pos <= size:
        left = 2 * pos
        right = left + 1
        smallest = pos
        current_key = elements[smallest - 1]['key']
        if left <= size:
            left_key = elements[left - 1]['key']
            if left_key < current_key:
                smallest = left
                current_key = left_key
        if right <= size:
            right_key = elements[right - 1]['key']
            if right_key < current_key:
                smallest = right
        if smallest == pos:
            return
        elements[pos - 1], elements[smallest - 1] = elements[smallest - 1], elements[pos - 1]
        pos = smallest


def insert(my_heap, value, key):
    my_heap['size'] += 1
    lt.add_last(my_heap['elements'], {'key': key, 'value': value})
    swim(my_heap, my_heap['size'])

def get_first_priority(my_heap):
    if my_heap['size'] == 0:
        return None
    return lt.first_element(my_heap["elements"])['value']

def remove(my_heap):
    if my_heap['size'] == 0:
        return None
    elements = my_heap['elements']['elements']
    max_priority_element = elements[0]
    last_element = elements.pop()
    my_heap['size'] -= 1
    if my_heap['size'] > 0:
        elements[0] = last_element
        sink(my_heap, 1)
    return max_priority_element['value']

