from pyxscat.h5_integrator import H5GIIntegrator
from pyxscat.h5_integrator import ROOT_DIRECTORY_KEY, FILENAME_H5_KEY, SAMPLE_GROUP_KEY, PONI_GROUP_KEY
from pyxscat.h5_integrator import PONIFILE_DATASET_KEY
from silx.io.h5py_utils import File
from pathlib import Path
import fabio
from pyxscat import PATH_PYXSCAT
import pytest
from pyFAI.io.ponifile import PoniFile

import pyautogui
from pyxscat.gui.run import run
from unittest.mock import patch

import time
import threading


from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtTest import QTest

from PyQt5.QtWidgets import QApplication
from pyxscat.gui.gui_window import GUIPyX_Window
import sys

from pyxscat.test.test_h5 import NCD_EXAMPLE_PATH, XMAS_EXAMPLE_PATH
# Open the GUI

EXAMPLE_PATH = XMAS_EXAMPLE_PATH
class TestGUI:

    @classmethod
    def setup_class(cls):
        print("Setting up setup class")

        cls.app = QApplication(sys.argv)
        cls.main_window = GUIPyX_Window()
        cls.main_window.show()
        cls.w = cls.main_window._guiwidget
        # cls.app.exec_()

    def test_qz_state(self):
        state_1 = self.w.state_qz

        button_widget = self.w.button_qz
        QTest.mouseClick(button_widget, Qt.LeftButton)

        state_2 = self.w.state_qz

        assert state_1 != state_2

    def test_qz_change(self):
        button_widget = self.w.button_qz
        QTest.mouseClick(button_widget, Qt.LeftButton)

        button_state = button_widget.isChecked()
        instance_state = self.w.state_qz

        assert button_state == instance_state

    def test_qr_state(self):
        state_1 = self.w.state_qr

        button_widget = self.w.button_qr
        QTest.mouseClick(button_widget, Qt.LeftButton)

        state_2 = self.w.state_qr

        assert state_1 != state_2

    def test_qr_change(self):
        button_widget = self.w.button_qr
        QTest.mouseClick(button_widget, Qt.LeftButton)

        button_state = button_widget.isChecked()
        instance_state = self.w.state_qr

        assert button_state == instance_state

    # @patch.object(self.app.QFileDialog, 'getExistingDirectory', return_value=NCD_EXAMPLE_PATH)
    def test_input_root_dir(self):
        button_widget = self.w.button_pick_rootdir
        threading.Thread(target=self.automate_directory_selection).start()

        QTest.mouseClick(button_widget, Qt.LeftButton)
        


    def automate_directory_selection(self):
        # Wait for the dialog to open
        QTest.qWait(5000)
        # Interact with QFileDialog
        pyautogui.write(str(Path(EXAMPLE_PATH)))
        # time.sleep(5)
        pyautogui.press('tab')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')


    def test_click_list_widget(self):
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.check_list_widget_state)
        self.poll_timer.start(100)

        listWidget = self.w.listwidget_samples

        for ind in range(listWidget.count()+1):
            self.click_list_widget(ind=ind)

        self.click_list_widget(ind=0)

    def click_list_widget(self, ind=0):
        listWidget = self.w.listwidget_samples

        item = listWidget.item(ind)
        listWidget.scrollToItem(item)        

        # Get the rectangle (position and size) of the item
        item_rect = listWidget.visualItemRect(item)
            
        # Calculate the global position of the center of the item
        global_pos = listWidget.mapToGlobal(item_rect.center())
        local_pos = listWidget.viewport().mapFromGlobal(global_pos)
            
        # Simulate the mouse click
        QTest.mouseClick(listWidget.viewport(), Qt.LeftButton, pos=local_pos)
        QTest.qWait(1000)

    def check_list_widget_state(self):
        if self.w.listwidget_samples.count() > 0:
            self.poll_timer.stop() 
    
    def test_click_table(self):
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.check_table_widget_state)
        self.poll_timer.start(100)

        tableWidget = self.w.table_files

        for row in range(tableWidget.rowCount()+2):
            item = tableWidget.item(row+1,0)
            tableWidget.scrollToItem(item)

            item_rect = tableWidget.visualItemRect(item)
            global_pos = tableWidget.mapToGlobal(item_rect.center())
            local_pos = tableWidget.viewport().mapFromGlobal(global_pos)
            QTest.mouseClick(tableWidget.viewport(), Qt.LeftButton, pos=local_pos)
            QTest.qWait(1000)

    def check_table_widget_state(self):
        if self.w.table_files.rowCount() > 0:
            self.poll_timer.stop()


    def test_active_integration(self):
        cb = self.w.combobox_integration
        cb.markItems(list_items=['complete', 'oop'])









    def test_final_wait(self):
        QTest.qWait(10000)
