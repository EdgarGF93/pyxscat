
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from pyxscat.gui.graphlayout import GraphLayout
import sys
import fabio
import numpy as np


class Graph(GraphLayout):
    def __init__(self, *args):
        super().__init__(*args)



    # def update_graphs(
    #     self,
    #     list_filenames:list,
    #     raw=False,
    #     reshape=False,
    #     q=False,
    #     integration=False,
    #     ):
    #     data = self._open_data(list_filenames=list_filenames)
    #     if raw:
    #         self._update_raw_graph(data=data)
    #     if reshape:
    #         pass
    #     if q:
    #         pass
    #     if integration:
    #         self._update_1d_graph(data=data)

    def _update_raw_graph(self, data:np.array, z_lims:list):
        graph_2D_widget = self.graph_raw_widget
        if graph_2D_widget.getGraphXLimits() == (0, 100) and graph_2D_widget.getGraphYLimits() == (0, 100):
            reset_zoom = True
        else:
            reset_zoom = False

        # z_lims = self.weak_lims(data=data)
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


    def _update_integration_graph(self, result):
        graph_1D_widget = self.graph_1D_widget
        graph_1D_widget.addCurve(
            x=result.radial,
            y=result.intensity,
            resetzoom=True,
        )




def main():
    app = QApplication(sys.argv)
    mw = QMainWindow()
    graph = Graph()
    mw.setCentralWidget(graph)
    mw.show()
    app.exec_()

if __name__ == "__main__":
    main()