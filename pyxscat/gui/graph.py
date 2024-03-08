
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from pyxscat.gui.graphlayout import GraphLayout
import sys
import fabio
import numpy as np


class Graph(GraphLayout):
    def __init__(self, *args):
        super().__init__(*args)


    def _update_raw_graph(self, data:np.array):
        graph_2D_widget = self.graph_raw_widget
        if graph_2D_widget.getGraphXLimits() == (0, 100) and graph_2D_widget.getGraphYLimits() == (0, 100):
            reset_zoom = True
        else:
            reset_zoom = False

        z_lims = self.weak_lims(data=data)
        graph_2D_widget.addImage(
            data=data,
            colormap={
                'name': 'viridis',
                'normalization': 'log',
                'autoscale': False,
                'vmin': z_lims[0],
                'vmax': z_lims[1],
            },
            resetzoom=reset_zoom,
        )

    def weak_lims(self, data):
        mn = np.nanmean(data)
        sd = np.nanstd(data)
        return (mn+0*sd, mn+3*sd)
    
    def _update_integration_graph(self, results:list):
        graph_1D_widget = self.graph_1D_widget
        for ind, result in enumerate(results):
            graph_1D_widget.addCurve(
                # x=result.radial,
                # y=result.intensity,
                x=result[1],
                y=result[0],
                resetzoom=True,
                legend=f"{ind}",
            )
            # graph_1D_widget.setGraphXLabel(label=result.unit)
            graph_1D_widget.setGraphYLabel(label="Intensity")




def main():
    app = QApplication(sys.argv)
    mw = QMainWindow()
    graph = Graph()
    mw.setCentralWidget(graph)
    mw.show()
    app.exec_()

if __name__ == "__main__":
    main()