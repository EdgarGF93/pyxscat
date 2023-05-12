from PyQt5.QtWidgets import QTableWidgetItem

def insert_columns(table, num=1, labels=[]):
    """
        Insert new column at the last position of the table
    """
    print(num)
    print(labels)
    if labels:
        for item in labels:
            table.insertColumn(table.columnCount())
            table.setHorizontalHeaderItem(
                table.columnCount() - 1, 
                QTableWidgetItem(item)
            )
        return
    else:
        for _ in range(num):
            table.insertColumn(table.columnCount())

def get_header(table):
    """
        Returns a list of strings with all the horizontal labels
    """
    return [table.takeHorizontalHeaderItem(ind).text() for ind in range(table.columnCount())]

def insert_header(table, ind_column, item):
    """
        Insert an item (label) in the header of the table
    """
    table.setHorizontalHeaderItem(ind_column, QTableWidgetItem(item))

def insert_rows(table, num=1):
    """
        Insert a new row in the table
    """
    for _ in range(num):
        table.insertRow(table.rowCount())

def update_cell(table, row_ind, column_ind, st=''):
    """
        Update a single cell in the table
    """
    if isinstance(st, str):
        pass
    else:
        st = str(st)

    table.setItem(row_ind, column_ind, QTableWidgetItem(st))

def update_column_names(table, labels=[], reset=False):
    """
        Update the header of the table
    """
    if reset:
        table.setColumnCount(0)

    insert_columns(table, len(labels) - table.columnCount())

    for ind, item in enumerate(labels):
        insert_header(table, ind, item)


def clicked_index(table):
    """
        Return a tuple with row, column of clicked item on the table
    """
    return (table.currentRow(), table.currentColumn())

def clicked_item(table):
    """
        Return the text from the table upon clicking
    """
    index = clicked_index(table)
    return table.item(index[0], index[1]).text()

def item(table, row, column):
    """
        Return the string from the table upon index
    """
    return table.item(row, column).text()

def row(table):
    """
        Return the row of clicked item
    """
    return table.currentRow()

def column(table):
    """
        Return the column of clicked item
    """
    return table.currentColumn()

def selected_items(table):
    """
        Return a list of tuples with the coordinates of selected files in the table
    """
    return [(table.row(item), table.column(item)) for item in table.selectedItems()]

def reset(table):
    """
        Clear the table by putting the row counter to zero
    """
    table.setRowCount(0)
    table.setColumnCount(0)