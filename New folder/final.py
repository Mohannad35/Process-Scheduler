import sys, os
# if hasattr(sys, 'frozen'):
#     os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

# from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import platform
import ctypes
from os import path

from PyQt5.uic import loadUiType

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"CPU_Scheduler.ui"))
# CPU_Scheduler, _ = loadUiType('CPU_Scheduler.ui')

class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.onlyInt = QIntValidator()
        self.setupUi(self)
        self.ui = FORM_CLASS
        self.tableWidget.setColumnCount(3)
        self.restrict_input()
        self.handle_buttons()

    def set_rows(self, widget_index):
        if widget_index == 0:
            self.Apply.clicked.connect(lambda: self.handle_line_edits_1())
        elif widget_index == 1:
            self.Apply.clicked.connect(lambda: self.handle_line_edits_2())
        elif widget_index == 2:
            self.Apply.clicked.connect(lambda: self.handle_line_edits_3())
        elif widget_index == 3:
            self.Apply.clicked.connect(lambda: self.handle_line_edits_4())
        

    def set_priority(self, page, Column_no):
        self.stackedWidget.setCurrentWidget(page)
        self.tableWidget.setColumnCount(Column_no)
        # widget_index = self.stackedWidget.currentIndex()
        # print(widget_index)
        # self.set_rows(widget_index)

    def handle_buttons(self):
        self.btn_1.clicked.connect(lambda: self.set_priority(self.page_1, 3))
        self.btn_2.clicked.connect(lambda: self.set_priority(self.page_2, 3))
        self.btn_3.clicked.connect(lambda: self.set_priority(self.page_3, 4))
        self.btn_4.clicked.connect(lambda: self.set_priority(self.page_4, 3))
        self.process_no_1.textChanged.connect(lambda: self.disable_ok())
        self.process_no_2.textChanged.connect(lambda: self.disable_ok())
        self.process_no_3.textChanged.connect(lambda: self.disable_ok())
        self.process_no_4.textChanged.connect(lambda: self.disable_ok())
        self.q_time.textChanged.connect(lambda: self.disable_ok())
        self.Apply.clicked.connect(lambda: self.handle_line_edits())
        # self.Apply.clicked.connect(lambda: self.handle_line_edits_2())
        # self.Apply.clicked.connect(lambda: self.handle_line_edits_3())
        # self.Apply.clicked.connect(lambda: self.handle_line_edits_4())
        self.Simulate.clicked.connect(lambda: self.simulate_1_handler())
        # self.simulate_2.clicked.connect(lambda: self.simulate_2_handler())
        # self.simulate_3.clicked.connect(lambda: self.simulate_3_handler())
        # self.simulate_4.clicked.connect(lambda: self.simulate_4_handler())
        # widget_index = self.stackedWidget.currentIndex()
        # self.set_rows(widget_index)
        
    def restrict_input(self):
        self.process_no_1.setValidator(self.onlyInt)
        self.process_no_2.setValidator(self.onlyInt)
        self.process_no_3.setValidator(self.onlyInt)
        self.process_no_4.setValidator(self.onlyInt)


        self.show()

    def handle_line_edits(self):
        # FCFS.n1 = int(self.process_no_1.text())
        widget_index = self.stackedWidget.currentIndex()
        if widget_index == 0:
            self.tableWidget.setRowCount(int(self.process_no_1.text()))
        elif widget_index == 1:
            self.tableWidget.setRowCount(int(self.process_no_2.text()))
        elif widget_index == 2:
            self.tableWidget.setRowCount(int(self.process_no_3.text()))
        elif widget_index == 3:
            self.tableWidget.setRowCount(int(self.process_no_4.text()))

# no of process variables connection to line edits ##############################
    def handle_line_edits_1(self):
        # FCFS.n1 = int(self.process_no_1.text())
        self.tableWidget.setRowCount(int(self.process_no_1.text()))

    def handle_line_edits_2(self):
        # Shortest_Job_First.N = int(self.process_no_2.text())
        self.tableWidget.setRowCount(int(self.process_no_2.text()))
        # Shortest_Job_First.preemptive = self.preemptive_1.isChecked()
    
    def handle_line_edits_3(self):
        # Priority_sched.N3 = int(self.process_no_3.text())
        self.tableWidget.setRowCount(int(self.process_no_3.text()))
        
        self.tableWidget.insertColumn(4)
        # Priority_sched.preemptive__2 = self.preemptive_2.isChecked()

    def handle_line_edits_4(self):
        # RR_sched.n4 = int(self.process_no_4.text())
        # RR_sched.q = float(self.q_time.text())
        self.tableWidget.setRowCount(int(self.process_no_4.text()))


    # disable ok button if no text ##############################
    def disable_ok(self):
        self.Apply.setEnabled(False)
        # self.ok_2.setEnabled(False)
        # self.ok_3.setEnabled(False)
        # self.ok_4.setEnabled(False)
        if len(self.process_no_1.text()) > 0:
            self.Apply.setEnabled(True)
        if len(self.process_no_2.text()) > 0:
            self.Apply.setEnabled(True)
        if len(self.process_no_3.text()) > 0:
            self.Apply.setEnabled(True)
        if ((len(self.process_no_4.text()) > 0) and (len(self.q_time.text()) > 0)):
            self.Apply.setEnabled(True)

    def Handler_Priority_simulate(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    input()


if __name__ == '__main__':
    main()