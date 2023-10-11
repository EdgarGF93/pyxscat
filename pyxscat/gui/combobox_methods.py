



def value(combobox):
    """
        Returns the string inside the combobox widget
    """
    return combobox.currentText()

def all_items(combobox):
    """
        Returns a list with all the available items in the combobox
    """
    num_items = combobox.count()
    list_items = [combobox.itemText(index) for index in range(num_items)]
    list_items.sort()
    return list_items

def insert(combobox, item):
    """
        Insert a new value in the combobox
    """
    combobox.insertItem(
        combobox.count(), item
    )

def clear(combobox):
    """
        Clear (reset) the combobox
    """
    combobox.clear()


def insert_list(combobox, list_items, reset=False):
    """
        Reset (or not) the combobox and insert a list of items
    """
    if reset:
        clear(combobox)
    for item in list_items:
        insert(combobox, item)

def set_text(combobox, text=str()):
    """
        Set the current value of the combobox to the text
    """
    combobox.setCurrentText(text)

