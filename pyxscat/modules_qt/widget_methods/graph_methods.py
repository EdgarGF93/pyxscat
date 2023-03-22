
def get_array(graph_widget):
    """
        Returns the array that is represented in the widget
    """
    return graph_widget.getImage().getData()

def get_zlims(graph_widget):
    """
        Returns the contrast limits of the graph
    """
    cm = graph_widget.getImage().getColormap()
    return cm['vmin'], cm['vmax']