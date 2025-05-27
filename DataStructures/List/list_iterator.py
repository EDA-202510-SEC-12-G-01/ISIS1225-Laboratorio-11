def iterator(my_list):
    list_type = my_list.get('type', None)
    if list_type == 'array_list':
        for element in my_list['elements']:
            yield element
    elif list_type == 'single_linked_list':
        current = my_list['first']
        while current is not None:
            yield current['info']
            current = current['next']
    else:
        raise TypeError("Tipo de lista no soportado")
