import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..')))

from DataStructures.List import single_linked_list as sll

def new_queue():
    return sll.new_list()

def enqueue(my_queue, element):
    sll.add_last(my_queue, element)
    return my_queue

def dequeue(my_queue):
    return sll.remove_first(my_queue)

def peek(my_queue):
    return sll.first_element(my_queue)

def is_empty(my_queue):
    return sll.is_empty(my_queue)

def size(my_queue): 
    return sll.size(my_queue)