

def all_items(listwidget):
    """
        Returns a list of strings with all the items in the list_widget
    """
    return [listwidget.item(x).text() for x in range(listwidget.count())]

def insert(listwidget, item, repeat_file=False):
    """
        Insert item in the list_widget, allow repetition or not
    """
    if not repeat_file and item in all_items(listwidget):
        return
    else:
        listwidget.insertItem(listwidget.count(), str(item))

def insert_list(listwidget, item_list, reset=False, repeat_file=False):
    """
        Insert a list of items in the list_widget
    """
    if reset:
        clear(listwidget)
    for item in item_list:
        insert(listwidget, item, repeat_file)

def clear(listwidget):
    """
        Reset the listwidget
    """
    listwidget.clear()

def click_values(listwidget):
    """
        Returns a list of strings with the selected values
    """
    return [file.text() for file in listwidget.selectedItems()]