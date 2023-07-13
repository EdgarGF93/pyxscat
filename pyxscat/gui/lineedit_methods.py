
DEFAULT_SEPARATOR = ','

def text(lineedit):
    """
        Returns the string or float (if its possible) inside the lineedit_widget
    """
    try:
        return int(lineedit.text())
    except:
        pass
    try:
        return float(lineedit.text())
    except:
        return str(lineedit.text())

def get_list(lineedit, separator=DEFAULT_SEPARATOR) -> list:
    """
        Returns the text of a line edit in the form of a list using a separator
    """
    return [item for item in text(lineedit=lineedit).split(separator) if item]

def insert(lineedit, new_text, repeat=False):
    """
        Insert new text at the end of the current text, separated with a comma
    """
    if not repeat and str(new_text) in text(lineedit):
        pass
    else:
        lineedit.setText(f"{text(lineedit)}{str(new_text)},")

def substitute(lineedit, new_text):
    """
        Clear and insert the new text
    """
    lineedit.clear()
    lineedit.setText(str(new_text))

def get_clean_list(lineedit, separator=','):
    list_split = [item for item in lineedit.text().strip().split(separator) if item]
    return list_split

def clear(lineedit):
    """
        Clear and insert the new text
    """
    lineedit.clear()

def get_clean_lineedit(lineedit_widget, separator=','):
    """
    Returns a clean list of values taken from a lineedit widget

    Parameters:
    lineedit_widget()
    """
    return [item for item in lineedit_widget.text().strip().split(separator) if item]