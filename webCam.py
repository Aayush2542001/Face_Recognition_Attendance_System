# PyQt imports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer, QTime, QDate
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QTableView, QAbstractItemView, QHeaderView

# other imports are already present in Functions.py
# my imports
import sys
import cv2
import multiprocessing
from datetime import datetime
from Functions import  *
import time

class UI_class(object):
    def __init__(self, MainWindow):
        # required calls
        self.setupUi(MainWindow)
        self.connectUI()

        # manual changes to UI
        self.RUN = False
        self.wrongDetectionButton.setEnabled(False)

        # tableWidgets
        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.tableWidget_2.setColumnWidth(0, 50)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.tableWidget_2.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget_2.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.tableWidget_3.setColumnWidth(0, 180)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget_3.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget_3.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget_3.verticalHeader().setVisible(False)
        self.tableWidget_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        header = self.tableWidget_3.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        # time
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def connectUI(self):
        # other
        self.guessedPersonLabel.setText("Stopped scanning")
        self.tabWidget.tabBarClicked.connect(self.outterTab_clicked)
        self.tabWidget_2.tabBarClicked.connect(self.innerTab_clicked)
        # buttons
        self.toggleCameraButton.clicked.connect(self.toggleCamera)
        self.wrongDetectionButton.clicked.connect(self.wrongDetection)
        self.scanFaceAddButton.clicked.connect(self.addFace)
        self.scanFaceEditButton.clicked.connect(self.editFace)
        self.deleteEntryButton.clicked.connect(self.deleteEntry)
        self.updateNameButton.clicked.connect(self.updateName)
        self.getReportButton.clicked.connect(self.getReport)
        self.resetFilterButton.clicked.connect(self.resetFilter)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1055)
        MainWindow.setSizeIncrement(QtCore.QSize(1920, 1080))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setSizeIncrement(QtCore.QSize(1920, 1080))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setSizeIncrement(QtCore.QSize(1920, 800))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.dateTimeLabel_2 = QtWidgets.QLabel(self.tab)
        self.dateTimeLabel_2.setGeometry(QtCore.QRect(590, 110, 211, 31))
        self.dateTimeLabel_2.setObjectName("dateTimeLabel_2")
        self.dateTimeLabel = QtWidgets.QLabel(self.tab)
        self.dateTimeLabel.setGeometry(QtCore.QRect(1360, 110, 151, 31))
        self.dateTimeLabel.setObjectName("dateTimeLabel")
        self.videoLabel = QtWidgets.QLabel(self.tab)
        self.videoLabel.setGeometry(QtCore.QRect(372, 170, 1152, 648))
        self.videoLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.videoLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.videoLabel.setLineWidth(7)
        self.videoLabel.setText("")
        self.videoLabel.setObjectName("videoLabel")
        self.dateTimeLabel_3 = QtWidgets.QLabel(self.tab)
        self.dateTimeLabel_3.setGeometry(QtCore.QRect(380, 40, 181, 121))
        self.dateTimeLabel_3.setText("")
        self.dateTimeLabel_3.setPixmap(
            QtGui.QPixmap("../../PycharmProjects/FaceRecognition/Extra/Face Recognition Image.png"))
        self.dateTimeLabel_3.setScaledContents(True)
        self.dateTimeLabel_3.setObjectName("dateTimeLabel_3")
        self.guessedPersonLabel = QtWidgets.QLabel(self.tab)
        self.guessedPersonLabel.setGeometry(QtCore.QRect(380, 850, 341, 31))
        self.guessedPersonLabel.setObjectName("guessedPersonLabel")
        self.toggleCameraButton = QtWidgets.QPushButton(self.tab)
        self.toggleCameraButton.setGeometry(QtCore.QRect(1360, 850, 151, 41))
        self.toggleCameraButton.setObjectName("toggleCameraButton")
        self.wrongDetectionButton = QtWidgets.QPushButton(self.tab)
        self.wrongDetectionButton.setGeometry(QtCore.QRect(1160, 850, 161, 41))
        self.wrongDetectionButton.setObjectName("wrongDetectionButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab_2)
        self.tabWidget_2.setGeometry(QtCore.QRect(420, 80, 1041, 521))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.label_9 = QtWidgets.QLabel(self.tab_9)
        self.label_9.setGeometry(QtCore.QRect(170, 50, 161, 16))
        self.label_9.setObjectName("label_9")
        self.empNameAddLineEdit = QtWidgets.QLineEdit(self.tab_9)
        self.empNameAddLineEdit.setGeometry(QtCore.QRect(350, 50, 281, 22))
        self.empNameAddLineEdit.setObjectName("empNameAddLineEdit")
        self.scanFaceAddButton = QtWidgets.QPushButton(self.tab_9)
        self.scanFaceAddButton.setGeometry(QtCore.QRect(680, 50, 111, 28))
        self.scanFaceAddButton.setObjectName("scanFaceAddButton")
        self.instructionLabel = QtWidgets.QLabel(self.tab_9)
        self.instructionLabel.setGeometry(QtCore.QRect(280, 140, 421, 171))
        self.instructionLabel.setObjectName("instructionLabel")
        self.tabWidget_2.addTab(self.tab_9, "")
        self.tab_10 = QtWidgets.QWidget()
        self.tab_10.setObjectName("tab_10")
        self.instructionLabel_2 = QtWidgets.QLabel(self.tab_10)
        self.instructionLabel_2.setGeometry(QtCore.QRect(140, 30, 421, 101))
        self.instructionLabel_2.setObjectName("instructionLabel_2")
        self.empNameEditLineEdit = QtWidgets.QLineEdit(self.tab_10)
        self.empNameEditLineEdit.setGeometry(QtCore.QRect(500, 190, 281, 22))
        self.empNameEditLineEdit.setObjectName("empNameEditLineEdit")
        self.scanFaceEditButton = QtWidgets.QPushButton(self.tab_10)
        self.scanFaceEditButton.setGeometry(QtCore.QRect(500, 310, 121, 28))
        self.scanFaceEditButton.setObjectName("scanFaceEditButton")
        self.label_10 = QtWidgets.QLabel(self.tab_10)
        self.label_10.setGeometry(QtCore.QRect(500, 160, 161, 16))
        self.label_10.setObjectName("label_10")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_10)
        self.tableWidget.setGeometry(QtCore.QRect(140, 160, 301, 291))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(149)
        self.updateNameButton = QtWidgets.QPushButton(self.tab_10)
        self.updateNameButton.setGeometry(QtCore.QRect(500, 220, 121, 28))
        self.updateNameButton.setObjectName("updateNameButton")
        self.tabWidget_2.addTab(self.tab_10, "")
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName("tab_11")
        self.deleteEntryButton = QtWidgets.QPushButton(self.tab_11)
        self.deleteEntryButton.setGeometry(QtCore.QRect(500, 160, 161, 28))
        self.deleteEntryButton.setObjectName("deleteEntryButton")
        self.instructionLabel_3 = QtWidgets.QLabel(self.tab_11)
        self.instructionLabel_3.setGeometry(QtCore.QRect(140, 30, 421, 101))
        self.instructionLabel_3.setObjectName("instructionLabel_3")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_11)
        self.tableWidget_2.setGeometry(QtCore.QRect(140, 160, 301, 291))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(149)
        self.tabWidget_2.addTab(self.tab_11, "")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(490, 200, 55, 16))
        self.label_2.setObjectName("label_2")
        self.volumeSlider = QtWidgets.QSlider(self.tab_3)
        self.volumeSlider.setGeometry(QtCore.QRect(710, 200, 160, 22))
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.clearDataButton = QtWidgets.QPushButton(self.tab_3)
        self.clearDataButton.setGeometry(QtCore.QRect(710, 330, 93, 28))
        self.clearDataButton.setObjectName("clearDataButton")
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(490, 330, 171, 16))
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(490, 260, 91, 16))
        self.label_3.setObjectName("label_3")
        self.exoprtDataButton = QtWidgets.QPushButton(self.tab_3)
        self.exoprtDataButton.setGeometry(QtCore.QRect(710, 250, 141, 28))
        self.exoprtDataButton.setObjectName("exoprtDataButton")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(490, 140, 55, 16))
        self.label.setObjectName("label")
        self.onRadio = QtWidgets.QRadioButton(self.tab_3)
        self.onRadio.setGeometry(QtCore.QRect(710, 140, 95, 20))
        self.onRadio.setObjectName("onRadio")
        self.offRadio = QtWidgets.QRadioButton(self.tab_3)
        self.offRadio.setGeometry(QtCore.QRect(790, 140, 95, 20))
        self.offRadio.setObjectName("offRadio")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.searchEmployeeLineEdit = QtWidgets.QLineEdit(self.tab_4)
        self.searchEmployeeLineEdit.setGeometry(QtCore.QRect(490, 40, 281, 22))
        self.searchEmployeeLineEdit.setObjectName("searchEmployeeLineEdit")
        self.label_11 = QtWidgets.QLabel(self.tab_4)
        self.label_11.setGeometry(QtCore.QRect(320, 40, 161, 16))
        self.label_11.setObjectName("label_11")
        self.getReportButton = QtWidgets.QPushButton(self.tab_4)
        self.getReportButton.setGeometry(QtCore.QRect(320, 130, 121, 28))
        self.getReportButton.setObjectName("getReportButton")
        self.resetFilterButton = QtWidgets.QPushButton(self.tab_4)
        self.resetFilterButton.setGeometry(QtCore.QRect(490, 130, 121, 28))
        self.resetFilterButton.setObjectName("resetFilterButton")
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget_3.setGeometry(QtCore.QRect(430, 200, 451, 751))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(3)
        self.tableWidget_3.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(149)
        self.label_12 = QtWidgets.QLabel(self.tab_4)
        self.label_12.setGeometry(QtCore.QRect(320, 90, 101, 16))
        self.label_12.setObjectName("label_12")
        self.dateEdit = QtWidgets.QDateEdit(self.tab_4)
        self.dateEdit.setDate(QDate(2000, 1, 1))
        self.dateEdit.setGeometry(QtCore.QRect(560, 90, 110, 22))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit_2 = QtWidgets.QDateEdit(self.tab_4)
        self.dateEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_2.setGeometry(QtCore.QRect(780, 90, 110, 22))
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.label_13 = QtWidgets.QLabel(self.tab_4)
        self.label_13.setGeometry(QtCore.QRect(490, 90, 81, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.tab_4)
        self.label_14.setGeometry(QtCore.QRect(710, 90, 61, 16))
        self.label_14.setObjectName("label_14")
        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.dateTimeLabel_2.setText(_translate("MainWindow", "Face detection attendance system"))
        self.dateTimeLabel.setText(_translate("MainWindow", "13 Aug, 2021 15:37"))
        self.guessedPersonLabel.setText(_translate("MainWindow", "Scanning mode"))
        self.toggleCameraButton.setText(_translate("MainWindow", "Toggle Camera"))
        self.wrongDetectionButton.setText(_translate("MainWindow", "Wrong Detection"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Main Window"))
        self.label_9.setText(_translate("MainWindow", "Enter Employee Name"))
        self.empNameAddLineEdit.setPlaceholderText(_translate("MainWindow", "Employee name"))
        self.scanFaceAddButton.setText(_translate("MainWindow", "Scan Face"))
        self.instructionLabel.setText(_translate("MainWindow",
                                                 "<html><head/><body><p>Instructions:</p><p>Step 1: Enter Employee\'s Name in <span style=\" font-weight:600;\">Text-Box</span></p><p>Step 2: Before clicking <span style=\" font-weight:600;\">Scan Face</span>, stand still in front of Webcam</p><p>Step 3: Once clicking the button, <span style=\" font-weight:600;\">move and</span><span style=\" font-weight:600;\">change your distance</span> by coming close and going far</p><p>Step 4: It will take <span style=\" font-weight:600;\">15 seconds</span> to scan your multiple faces</p><p>Step 5: You will be notified by <span style=\" font-weight:600;\">success message</span></p><p><br/></p></body></html>"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_9),
                                    _translate("MainWindow", "Add Employee Entry"))
        self.instructionLabel_2.setText(_translate("MainWindow",
                                                   "<html><head/><body><p>Instructions:</p><p>Step 1: <span style=\" font-weight:600;\">Select</span> Employee name from List</p><p>Step 2: Edit <span style=\" font-weight:600;\">Employee name</span> and/or <span style=\" font-weight:600;\">Scan Face</span> by clicking appropriate</p><p>Step 3: You will see <span style=\" font-weight:600;\">success message</span> after the update process</p></body></html>"))
        self.empNameEditLineEdit.setPlaceholderText(_translate("MainWindow", "Employee name"))
        self.scanFaceEditButton.setText(_translate("MainWindow", "Re-Scan Face"))
        self.label_10.setText(_translate("MainWindow", "Re-Enter Employee Name"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Employee Name"))
        self.updateNameButton.setText(_translate("MainWindow", "Upate Name"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_10),
                                    _translate("MainWindow", "Edit employee Entry"))
        self.deleteEntryButton.setText(_translate("MainWindow", "Delete Selected Entry"))
        self.instructionLabel_3.setText(_translate("MainWindow",
                                                   "<html><head/><body><p>Instructions:</p><p>Step 1: <span style=\" font-weight:600;\">Select</span> Employee name from List</p><p>Step 2: Click <span style=\" font-weight:600;\">Delete Entry </span>button</p><p>Step 3: You will see <span style=\" font-weight:600;\">success message</span> after the deletino process</p></body></html>"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Employee Name"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_11),
                                    _translate("MainWindow", "Delete Employee Entry"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Edit Employee Details"))
        self.label_2.setText(_translate("MainWindow", "Volume"))
        self.clearDataButton.setText(_translate("MainWindow", "Clear"))
        self.label_5.setText(_translate("MainWindow", "Clear Data/ Reset Application"))
        self.label_3.setText(_translate("MainWindow", "Export Data"))
        self.exoprtDataButton.setText(_translate("MainWindow", "Export to local disk"))
        self.label.setText(_translate("MainWindow", "Sound"))
        self.onRadio.setText(_translate("MainWindow", "On"))
        self.offRadio.setText(_translate("MainWindow", "Off"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Settings"))
        self.searchEmployeeLineEdit.setPlaceholderText(_translate("MainWindow", "Employee name"))
        self.label_11.setText(_translate("MainWindow", "Filter by employee"))
        self.getReportButton.setText(_translate("MainWindow", "Get report"))
        self.resetFilterButton.setText(_translate("MainWindow", "Reset filters"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Employee Name"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Worked Hours (Hour:Min:Sec)"))
        self.label_12.setText(_translate("MainWindow", "Filter by date"))
        self.label_13.setText(_translate("MainWindow", "Start date"))
        self.label_14.setText(_translate("MainWindow", "End date"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Report and statistics"))


    def outterTab_clicked(self, index):
        if index == 3:
            self.setReportTable()
        else:
            return

    def getReport(self):
        self.setReportTable()

    def resetFilter(self):
        self.dateEdit.setDate(QDate(2000, 1, 1))
        self.dateEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())
        self.setReportTable()

    def setReportTable(self):
        startDate = self.dateEdit.date().toPyDate()
        endDate = self.dateEdit_2.date().toPyDate()
        IdNameHourList = Database.getWorkedTimeManually(startDate, endDate)
        self.tableWidget_3.clear()
        self.tableWidget_3.setHorizontalHeaderLabels(["ID", "Employee Name", "Worked Hours (Hour:Min:Sec)"])
        self.tableWidget_3.setRowCount(len(IdNameHourList))
        for i in range(len(IdNameHourList)):
            self.tableWidget_3.setItem(i, 0, QTableWidgetItem(IdNameHourList[i][0]))
            self.tableWidget_3.setItem(i, 1, QTableWidgetItem(IdNameHourList[i][1]))
            self.tableWidget_3.setItem(i, 2, QTableWidgetItem(IdNameHourList[i][2]))

    def innerTab_clicked(self, index):
        if index == 1:
            Widget = self.tableWidget
        elif index == 2:
            Widget = self.tableWidget_2
        else:
            return
        IdNameList = Database.getIdNames()
        Widget.clear()
        Widget.setHorizontalHeaderLabels(["ID", "Employee Name"])
        Widget.setRowCount(len(IdNameList))
        for i in range(len(IdNameList)):
            Widget.setItem(i, 0, QTableWidgetItem(IdNameList[i][0]))
            Widget.setItem(i, 1, QTableWidgetItem(IdNameList[i][1]))

    def displayTime(self):
        self.dateTimeLabel.setText(datetime.strftime(datetime.now(), "%d-%m-%y\n%H:%M:%S"))

    def toggleCamera(self):
        self.RUN = not self.RUN
        if self.RUN:
            self.guessedPersonLabel.setText("Scanning mode")
            self.showVideoAndDetectFace()
        else:
            # show wallpaper
            self.guessedPersonLabel.setText("Stopped scanning")
            self.wrongDetectionButton.setEnabled(False)

    def wrongDetection(self):
        pass

    def addFace(self):
        if self.empNameAddLineEdit.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Validation")
            msg.setText("Name field is empty")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            empName = self.empNameAddLineEdit.text()

            # storing encode
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            EncodeList = []
            while len(EncodeList) < 8:
                noError, frame = cap.read()
                if noError:
                    encode = face_recognition.face_encodings(frame)
                    if encode:
                        EncodeList.append(encode[0])
                    else:
                        continue
                else:
                    continue
                cv2.waitKey(250)
            saveEncodes(empName,EncodeList)
            cap.release()
            cv2.destroyAllWindows()

            # storing name to database
            id = Database.addEmployee(empName)

            # clearing text of textEdit
            self.empNameAddLineEdit.setText("")

            # success msg
            msg = QMessageBox()
            msg.setWindowTitle("Successful")
            msg.setText(f"Entry successful\nID = {id}\nUsername = {empName}") # / also show number and name
            msg.setIcon(QMessageBox.Information)
            msg.exec_()

    def editFace(self):
        try:
            empName = self.tableWidget.selectionModel().selectedIndexes()[1].data()

            # storing encode
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            updatedEncode = []
            while len(updatedEncode) < 8:
                noError, frame = cap.read()
                if noError:
                    encode = face_recognition.face_encodings(frame)
                    if encode:
                        updatedEncode.append(encode[0])
                    else:
                        continue
                else:
                    continue
                cv2.waitKey(250)
            cap.release()
            cv2.destroyAllWindows()

            # updating encodes from file
            updateEncodes(empName,updatedEncode)

            IdNameList = Database.getIdNames()
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Employee Name"])
            self.tableWidget.setRowCount(len(IdNameList))
            for i in range(len(IdNameList)):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(IdNameList[i][0]))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(IdNameList[i][1]))

            # success msg
            msg = QMessageBox()
            msg.setWindowTitle("Successful")
            msg.setText("Face updated successfully")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Validation")
            msg.setText("Make sure to select the item")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def updateName(self):
        try:
            idToUpdate = self.tableWidget.selectionModel().selectedIndexes()[0].data()
            oldName = self.tableWidget.selectionModel().selectedIndexes()[1].data()
            updatedName = self.empNameEditLineEdit.text()

            # updating from database
            Database.updateById(idToUpdate,updatedName)
            # update encode file name
            updateEncodeFileName(oldName,updatedName)

            IdNameList = Database.getIdNames()
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Employee Name"])
            self.tableWidget.setRowCount(len(IdNameList))
            for i in range(len(IdNameList)):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(IdNameList[i][0]))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(IdNameList[i][1]))

            self.empNameEditLineEdit.setText("")

            # success msg
            msg = QMessageBox()
            msg.setWindowTitle("Successful")
            msg.setText("Item updated successfully")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Validation")
            msg.setText("Make sure to select the item")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def deleteEntry(self):
        try:
            idToDelete = self.tableWidget_2.selectionModel().selectedIndexes()[0].data()
            encodeToDelete = self.tableWidget_2.selectionModel().selectedIndexes()[1].data()

            # deleting from database
            Database.deleteById(idToDelete)
            # deleting encodes from file
            deleteEncode(encodeToDelete)

            IdNameList = Database.getIdNames()
            self.tableWidget_2.clear()
            self.tableWidget_2.setHorizontalHeaderLabels(["ID", "Employee Name"])
            self.tableWidget_2.setRowCount(len(IdNameList))
            for i in range(len(IdNameList)):
                self.tableWidget_2.setItem(i, 0, QTableWidgetItem(IdNameList[i][0]))
                self.tableWidget_2.setItem(i, 1, QTableWidgetItem(IdNameList[i][1]))

            # success msg
            msg = QMessageBox()
            msg.setWindowTitle("Successful")
            msg.setText("Item deleted successfully")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Validation")
            msg.setText("Make sure to select the item")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def showVideoAndDetectFace(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        faceDetectProcess = multiprocessing.Process(target=testFrameProcess)
        faceDetectProcess.start()

        while self.RUN:
            noError, frame = cap.read()
            if noError:
                self.displayFrameToLabel(frame)
                write(os.getcwd() + "\\Pickle\\FaceDetectObjects\\frame.pickle",frame)

                detectedPerson = read(minPersonPath)
                if detectedPerson != "Scanning mode":
                    returnDate = Database.attendance(detectedPerson)
                    self.guessedPersonLabel.setText(f"{detectedPerson}'s attendance successfully taken on {returnDate}")
                    self.guessedPersonLabel.adjustSize()
                    self.wrongDetectionButton.setEnabled(True)
                else:
                    self.guessedPersonLabel.setText(detectedPerson)
                    self.wrongDetectionButton.setEnabled(False)
                cv2.waitKey(0)

        faceDetectProcess.terminate()
        cap.release()
        cv2.destroyAllWindows()

    def displayFrameToLabel(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        frame = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        self.videoLabel.setPixmap(QPixmap.fromImage(frame))
        self.videoLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # setAlignment -> align image at center of label
        # setPixmap -> set label as image
        # bytesPerLine -> RGB = 3, RGBA = 4


if __name__ == "__main__":
    # other statements
    # print(Database.getWorkedTimeManually())
    # exit()

    app = QtWidgets.QApplication(sys.argv)
    css = """ """
    app.setStyleSheet(css)
    MainWindow = QtWidgets.QMainWindow()
    UI = UI_class(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# Current work->settings

# Next work->Wrong detection button
# Wrong detection button should be on right side of screen
# when pressed video should be paused
# A list will appear below that button like in Add,Update and delete
# User will select a item from it and then OK button
# Do rest of work

# Next work->"CSS" or "Statistics design and coding"