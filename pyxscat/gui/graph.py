
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from pyxscat.gui.graphlayout import GraphLayout
import sys



class Graph(GraphLayout):
    pass





def main():
    app = QApplication(sys.argv)
    mw = QMainWindow()
    graph = Graph()
    mw.setCentralWidget(graph)
    mw.show()
    app.exec_()

if __name__ == "__main__":
    main()