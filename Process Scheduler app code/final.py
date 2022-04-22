import sys, os
from time import time_ns
# if hasattr(sys, 'frozen'):
#     os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

import Priority_module
import RR_module
import SJF_module

# from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import platform
import ctypes
from os import path, times_result

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

    # def set_rows(self, widget_index):
    #     if widget_index == 0:
    #         self.Apply.clicked.connect(lambda: self.handle_line_edits_1())
    #     elif widget_index == 1:
    #         self.Apply.clicked.connect(lambda: self.handle_line_edits_2())
    #     elif widget_index == 2:
    #         self.Apply.clicked.connect(lambda: self.handle_line_edits_3())
    #     elif widget_index == 3:
    #         self.Apply.clicked.connect(lambda: self.handle_line_edits_4())
        

    def set_priority(self, page, Column_no):
        self.stackedWidget.setCurrentWidget(page)
        self.tableWidget.setColumnCount(Column_no)
        if page == 2:
            self.tableWidget.setHorizontalHeaderLabels(['Process Name', 'Arrival Time', 'BurstTime (ms)', 'Priority'])
        # widget_index = self.stackedWidget.currentIndex()
        # print(widget_index)
        # self.set_rows(widget_index)

    def Handle_simulate_btn(self):
        widget_index = self.stackedWidget.currentIndex()
        if widget_index == 0:
            # FCFS
            pass
        elif widget_index == 1:
            # SJF
            self.Handler_SJF_simulate()
        elif widget_index == 2:
            # Priority
            self.Handler_Priority_simulate()
        elif widget_index == 3:
            # RR
            self.Handler_RoundRobin_simulate()

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
        self.Simulate.clicked.connect(lambda: self.Handle_simulate_btn())
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
        self.q_time.setValidator(self.onlyInt)


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
            Priority_module.NumberofProcesses = int(self.process_no_3.text())
            Priority_module.preemptive_orNot = self.preemptive_2.isChecked()
        elif widget_index == 3:
            self.tableWidget.setRowCount(int(self.process_no_4.text()))
            RR_module.NumberofProcesses = int(self.process_no_4.text())
            RR_module.q = int(self.q_time.text())

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
        Priority_module.NumberofProcesses = int(self.process_no_3.text())
        Priority_module.preemptive_orNot = self.preemptive_2.isChecked()
        
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

    def Handler_SJF_simulate(self):
        # try:
        #inputs
        NumberofProcesses = int(self.process_no_2.text())
        processList = []
        for i in range(int(NumberofProcesses)): 
            arrival = self.tableWidget.item(i, 1).text()
            burst = self.tableWidget.item(i, 2).text()
            processList.append(SJF_module.Process(name= i+1, arrival_time= arrival, burst_time= burst))
        Sjf = SJF_module.SJFPreemptive(processes= processList, preemptive= self.preemptive_1.isChecked())
        #output
        # Priority_module.Handler_ganttPriorityCalc()
        # self.Chart_priority()
        Sjf.run()
        self.Chart_SJF(Sjf)
            

        # except Exception as e:
        #     ctypes.windll.user32.MessageBoxW(0, "Data entered is incomplete or invalid.", "Error", 1)

    def Handler_Priority_simulate(self):
        try:
            #inputs
            Priority_module.processList.clear()
            for i in range(int(Priority_module.NumberofProcesses)): 
                arrival = self.tableWidget.item(i, 1).text()
                burst = self.tableWidget.item(i, 2).text()
                priority = self.tableWidget.item(i, 3).text()
                Priority_module.processList.append(Priority_module.process(Pid= i+1, burstTime= burst, arrivalTime= arrival, priority= priority))
            #output
            Priority_module.Handler_ganttPriorityCalc()
            self.Chart_priority()

        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, "Data entered is incomplete or invalid.", "Error", 1)

    def Handler_RoundRobin_simulate(self):
        try:
            #inputs
            while not (RR_module.inputQueue_RR.empty()):
                k = RR_module.inputQueue_RR.get()
            for i in range(int(RR_module.NumberofProcesses)):
                arrival = self.tableWidget.item(i, 1).text()
                burst = self.tableWidget.item(i, 2).text()
                p = RR_module.process(i + 1, burst, arrival)
                RR_module.inputQueue_RR.put(p)
            #output
            RR_module.Handler_ganttRoundRobinCalc()
            self.Chart_RR()
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, "Data entered is incomplete or invalid.", "Error", 1)

    ############################################ Charts ###############################################
    def Chart_SJF(self, processes):
        graph = processes.get_graph()
        scene = QGraphicsScene()
        whiteBrush = QBrush(Qt.white)
        redPen = QPen(Qt.blue)
        redPen.setWidth(3)
        #draw
        f = 860 / SJF_module.time_sjf  #drawing factor
        print("total time =",SJF_module.time_sjf)
        time = float(graph[0][1])
        for s in (graph):
            if(float(s[1]) > time):
                item = scene.addText(str(time), QFont('Arial', 11))
                item.setPos(time * f - 12, 100)
                time = s[1]
            rect = scene.addRect(time * f, 50, (float(s[2])-float(s[1])) * f, 40, redPen, whiteBrush)
            #texts:
            item = scene.addText(self.tableWidget.item(int(s[0])-1, 0).text(), QFont('Arial', 13))
            item.setPos((time + ((float(s[2])-float(s[1])) / 2)) * f - 6, 57)
            item = scene.addText(str(round(time,3)), QFont('Arial', 11))
            item.setPos((time) * f - 12, 100)
            time += (float(s[2])-float(s[1]))
            print("time =",time)
        # last departure time text
        item = scene.addText(str(round(time,3)), QFont('Arial', 11))
        item.setPos(time * f - 12, 100)
        self.graphicsView_3.setScene(scene)
        self.graphicsView_3.show()
        self.waiting_time.setText(str(processes.get_average_waiting_time())+ " ms")

    def Chart_priority(self):
        scene = QGraphicsScene()
        whiteBrush = QBrush(Qt.white)
        redPen = QPen(Qt.blue)
        redPen.setWidth(3)
        #draw
        f = 860 / Priority_module.time  #drawing factor
        time = (Priority_module.outputPriority)[0]['arrival']
        for s in (Priority_module.outputPriority):
            if(s['arrival'] > time):
                item = scene.addText(str(time), QFont('Arial', 11))
                item.setPos(time * f - 12, 100)
                time = s['arrival']
            rect = scene.addRect(time * f, 50, s['length'] * f, 40, redPen, whiteBrush)
            #texts:
            item = scene.addText(self.tableWidget.item(s['process']-1, 0).text(), QFont('Arial', 13))
            item.setPos((time + (s['length'] / 2)) * f - 6, 57)
            item = scene.addText(str(round(time,3)), QFont('Arial', 11))
            item.setPos((time) * f - 12, 100)            
            time += s['length']
        # last departure time text
        item = scene.addText(str(round(time,3)), QFont('Arial', 11))
        item.setPos(time * f - 12, 100)
        self.graphicsView_3.setScene(scene)
        self.graphicsView_3.show()
        self.waiting_time.setText(str(Priority_module.avgWaitingTimePriority)+ " ms")

    def Chart_RR(self):
        scene = QGraphicsScene()
        whiteBrush = QBrush(Qt.white)
        bluePen = QPen(Qt.blue)
        bluePen.setWidth(3)
        #draw
        f = 860 / RR_module.totalBurstTime_RR  #drawing factor
        time = list(RR_module.outputQueue_RR.queue)[0]['arrival']
        for s in list(RR_module.outputQueue_RR.queue):
            if(s['arrival'] > time):
                item = scene.addText(str(round(time,3)), QFont('Arial', 11))
                item.setPos(time * f - 12, 100)
                time = s['arrival']
            rect = scene.addRect(time * f, 50, s['slice'] * f, 40, bluePen, whiteBrush)
            #texts:
            item = scene.addText(self.tableWidget.item(s['pid']-1, 0).text(), QFont('Arial', 13))
            item.setPos((time + (s['slice'] / 2)) * f - 6, 57)
            item = scene.addText(str(round(time,3)), QFont('Arial', 11))
            item.setPos((time) * f - 12, 100)            
            time += s['slice']
        # last departure time text
        item = scene.addText(str(round(time,3)), QFont('Arial', 11))
        item.setPos(time * f - 12, 100)        
        self.graphicsView_3.setScene(scene)
        self.graphicsView_3.show()
        self.waiting_time.setText(str(RR_module.avgWaitingTime_RoundRobin)+ " ms")


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    input()


if __name__ == '__main__':
    main()