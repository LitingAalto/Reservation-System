import sys
from datetime import datetime, timedelta
import pandas as pd
import calendar
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QTableView
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont
from PyQt5.QtCore import QDate, Qt, QAbstractTableModel
from doctor import Doctor
from customer import Customer


class ReservationSystem(QWidget):
    global currentYear, currentMonth, currentDay

    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    dic = {'teeth check up': ['Kaisa', 'Teemu', 'Inka'],
           'teeth removal': ['Kaisa', 'Teemu', 'Inka'],
           'teeth whitening': ['Kaisa', 'Teemu', 'Inka'],
           'consultation': ['Kaisa', 'Inka'],
           'implant': ['Inka']}

    service_time = {'teeth check up': 25,
                    'teeth removal': 25,
                    'teeth whitening': 25,
                    'consultation': 20,
                    'implant': 55}

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Reservation System')
        self.setGeometry(300, 200, 1000, 800)
        self.model = QStandardItemModel()
        # Calendar
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.setGeometry(20, 250, 460, 330)
        self.init_calendar()
        # menu bar
        self.menubar = QtWidgets.QMenuBar(self)
        # self.menubar.setGeometry(0, 0, 600, 10)
        self.menuOther_services = QtWidgets.QMenu(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.actionCheck_history = QtWidgets.QAction(self)
        self.actionCheck_history.setText("Get booking records")
        self.menuOther_services.addAction(self.actionCheck_history)
        self.actionCancellation = QtWidgets.QAction(self)
        self.actionCancellation.setText("Cancellation")
        self.menuOther_services.addAction(self.actionCancellation)
        self.menuOther_services.setTitle("Other services")
        self.menubar.addAction(self.menuOther_services.menuAction())
        self.actionCheck_history.triggered.connect(self.history_window)
        self.actionCancellation.triggered.connect(self.cancellation_window)
        # Name
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Name")
        self.label1.setGeometry(20, 50, 200, 20)
        self.name = QtWidgets.QLineEdit(self)
        self.name.setGeometry(20, 70, 200, 20)
        self.name.setPlaceholderText("Enter Your Name")
        # Email
        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("Email")
        self.label2.setGeometry(260, 50, 200, 20)
        self.email = QtWidgets.QLineEdit(self)
        self.email.setGeometry(260, 70, 200, 20)
        self.email.setPlaceholderText("Enter your Email")
        # Phone
        self.label3 = QtWidgets.QLabel(self)
        self.label3.setText("Phone")
        self.label3.setGeometry(500, 50, 200, 20)
        self.phone = QtWidgets.QLineEdit(self)
        self.phone.setGeometry(500, 70, 200, 20)
        self.phone.setPlaceholderText("Phone number starting with 0")
        # Select Service
        self.label4 = QtWidgets.QLabel(self)
        self.label4.setText("Select Service")
        self.label4.setGeometry(20, 115, 200, 20)
        self.service = QtWidgets.QComboBox(self)
        self.service.setGeometry(20, 145, 200, 30)
        self.service.setModel(self.model)
        # label text 1
        self.label5 = QtWidgets.QLabel(self)
        self.label5.setText(
            "Click on the date and available slots will shown on the right=>\nALWAYS click on the date to REFRESH the "
            "available slots!")
        self.label5.setGeometry(20, 200, 500, 40)
        # Select Doctor
        self.label5 = QtWidgets.QLabel(self)
        self.label5.setText("Select Doctor")
        self.label5.setGeometry(260, 115, 200, 20)
        self.doctor = QtWidgets.QComboBox(self)
        self.doctor.setGeometry(260, 145, 200, 30)
        self.doctor.setModel(self.model)
        # update combobox
        self.update_combobox()
        # time list
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(520, 180, 200, 400)
        # label text 2
        self.label6 = QtWidgets.QLabel(self)
        self.label6.setText("Pick a time below")
        self.label6.setGeometry(515, 140, 180, 20)
        # Button and checkbox
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(240, 660, 80, 30)
        self.pushButton.setText("Reserve")
        self.checkBox = QtWidgets.QCheckBox(self)
        self.checkBox.setGeometry(50, 615, 600, 50)
        self.checkBox.setText("I confirm all information are correct and I want to reserve this time")
        # Reserve time
        self.pushButton.clicked.connect(self.reserve)
        # reminder label in red color
        self.label7 = QtWidgets.QLabel(self)
        self.label7.setGeometry(100, 700, 500, 30)
        # New window after reservation
        self.window = QtWidgets.QMainWindow()
        self.window.resize(550, 300)
        self.window.setWindowTitle("Your booking is complete!")
        self.window.label = QtWidgets.QLabel(self.window)
        self.window.label.setGeometry(55, 30, 450, 200)
        self.show()
        # New window for history
        self.window2 = QtWidgets.QMainWindow()
        self.window2.resize(700, 600)
        self.window2.setWindowTitle("Get booking records")
        self.window2.label = QtWidgets.QLabel(self.window2)
        self.window2.label.setGeometry(20, 10, 650, 40)
        self.window2.label.setText("Please enter your information to check booking records.\nRecords will be returned "
                                   "only if name and phone are matched with the records")
        # Name 2
        self.window2.label1 = QtWidgets.QLabel(self.window2)
        self.window2.label1.setText("Name")
        self.window2.label1.setGeometry(20, 70, 150, 20)
        self.window2.name = QtWidgets.QLineEdit(self.window2)
        self.window2.name.setGeometry(20, 90, 150, 20)
        self.window2.name.setPlaceholderText("Enter Your Name")
        # Phone 2
        self.window2.label3 = QtWidgets.QLabel(self.window2)
        self.window2.label3.setText("Phone")
        self.window2.label3.setGeometry(200, 70, 150, 20)
        self.window2.phone = QtWidgets.QLineEdit(self.window2)
        self.window2.phone.setGeometry(200, 90, 150, 20)
        self.window2.phone.setPlaceholderText("Phone number")
        # Button and checkbox
        self.window2.pushButton = QtWidgets.QPushButton(self.window2)
        self.window2.pushButton.setGeometry(380, 80, 150, 30)
        self.window2.pushButton.setText("Get records")
        # qtableview
        self.window2.tableWidget = QtWidgets.QTableWidget(self.window2)
        self.window2.tableWidget.setGeometry(10, 140, 500, 400)
        self.window2.labeln = QtWidgets.QLabel(self.window2)
        self.window2.pushButton.clicked.connect(self.display_history)

        # New window if want cancellation
        self.window3 = QtWidgets.QMainWindow()
        self.window3.resize(960, 600)
        self.window3.setWindowTitle("cancellation")
        self.window3.label = QtWidgets.QLabel(self.window3)
        self.window3.label.setGeometry(15, 10, 550, 20)
        self.window3.label.setText("Please enter your information for cancellation.")
        self.window3.label2 = QtWidgets.QLabel(self.window3)
        self.window3.label2.setGeometry(15, 25, 550, 20)
        self.window3.label2.setStyleSheet("color: red")
        self.window3.label2.setText("Please note for cancellation within 24 hours, you will be charged 40€!")
        self.window3.label3 = QtWidgets.QLabel(self.window3)
        self.window3.label3.setGeometry(600, 20, 550, 100)
        self.window3.label3.setText(
            "Select the time you would like\n to cancel by checking the 'Cancel' box.\nOnce the "
            "below button is clicked, \nyour cancellation request will be handled")
        # Name
        self.window3.label1 = QtWidgets.QLabel(self.window3)
        self.window3.label1.setText("Name")
        self.window3.label1.setGeometry(20, 70, 150, 20)
        self.window3.name = QtWidgets.QLineEdit(self.window3)
        self.window3.name.setGeometry(20, 90, 150, 20)
        self.window3.name.setPlaceholderText("Enter Your Name")
        # Phone
        self.window3.label3 = QtWidgets.QLabel(self.window3)
        self.window3.label3.setText("Phone")
        self.window3.label3.setGeometry(200, 70, 150, 20)
        self.window3.phone = QtWidgets.QLineEdit(self.window3)
        self.window3.phone.setGeometry(200, 90, 150, 20)
        self.window3.phone.setPlaceholderText("Phone number")
        # Button
        self.window3.pushButton = QtWidgets.QPushButton(self.window3)
        self.window3.pushButton.setGeometry(380, 80, 120, 30)
        self.window3.pushButton.setText("Search/Refresh")
        # qtableview
        self.window3.tableWidget = QtWidgets.QTableWidget(self.window3)
        self.window3.tableWidget.setGeometry(5, 140, 600, 400)
        self.window3.labeln = QtWidgets.QLabel(self.window3)
        # cancellation button
        self.window3.cancel = QtWidgets.QPushButton(self.window3)
        self.window3.cancel.setGeometry(640, 150, 150, 30)
        self.window3.cancel.setText("Confirm Cancel")
        # Cancelation confirmation text
        self.window3.label4 = QtWidgets.QLabel(self.window3)
        self.window3.label4.setGeometry(620, 190, 350, 60)
        self.window3.pushButton.clicked.connect(self.cancellation)
        self.window3.cancel.clicked.connect(self.cancellation_click)

    def history_window(self):
        self.window2.labeln.clear()
        self.window2.name.clear()
        self.window2.phone.clear()
        self.window2.tableWidget.clear()
        self.window2.show()

    def cancellation_window(self):
        self.window3.name.clear()
        self.window3.phone.clear()
        self.window3.labeln.clear()
        self.window3.label4.clear()
        self.window3.tableWidget.clear()
        self.window3.show()

    def cancellation_click(self):
        name = self.window3.name.text()
        phone = "'" + self.window3.phone.text()
        c = Customer(name, phone)
        for i in range(self.window3.tableWidget.rowCount()):
            item = self.window3.tableWidget.item(i, self.window3.tableWidget.columnCount() - 1)
            if item.checkState() != 0:
                date = self.window3.tableWidget.item(item.row(), 0)
                time = self.window3.tableWidget.item(item.row(), 1)
                doctor = self.window3.tableWidget.item(item.row(), 2)
                service = self.window3.tableWidget.item(item.row(), 3)
                txt = c.cancel(date.text(), time.text(), service.text(), doctor.text())
                self.window3.label4.setText(txt + '\nhit search/refresh to refresh booking records!')

    def display_history(self):
        self.window2.tableWidget.clear()
        name = self.window2.name.text()
        phone = "'" + self.window2.phone.text()
        df = Customer.get_booked(name, phone)
        if isinstance(df, pd.DataFrame):
            self.window2.labeln.clear()
            df = df[['Reserved date', 'Reserved time', 'Reserved doctor', 'Reserved service']].drop_duplicates()
            df = df.sort_values(['Reserved date', 'Reserved time'], ascending=[True, True])
            self.window2.tableWidget.setRowCount(df.shape[0])
            self.window2.tableWidget.setColumnCount(df.shape[1])
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    item = QtWidgets.QTableWidgetItem(str(df.iloc[i, j]))
                    self.window2.tableWidget.setItem(i, j, item)
            self.window2.tableWidget.setHorizontalHeaderLabels(df.columns.tolist())
        else:
            self.window2.labeln.setText("Record not found! Please input valid name and phone!")
            self.window2.labeln.setStyleSheet("color: red")
            self.window2.labeln.setGeometry(40, 114, 400, 20)

    def cancellation(self):
        self.window3.labeln.clear()
        self.window3.tableWidget.clear()
        self.window3.label4.clear()
        name = self.window3.name.text()
        phone = "'" + self.window3.phone.text()
        df = Customer.get_future_events(name, phone)
        if isinstance(df, pd.DataFrame):
            self.window3.labeln.clear()
            df = df[['Reserved date', 'Reserved time', 'Reserved doctor', 'Reserved service']].drop_duplicates()
            df = df.sort_values(['Reserved date', 'Reserved time'], ascending=[True, True])
            self.window3.tableWidget.setRowCount(df.shape[0])
            self.window3.tableWidget.setColumnCount(df.shape[1])
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    item = QtWidgets.QTableWidgetItem(str(df.iloc[i, j]))
                    self.window3.tableWidget.setItem(i, j, item)
            # add one column for checkbox
            self.window3.tableWidget.insertColumn(df.shape[1])
            for i in range(df.shape[0]):
                chkBoxItem = QtWidgets.QTableWidgetItem()
                chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                self.window3.tableWidget.setItem(i, df.shape[1], chkBoxItem)
            self.window3.tableWidget.setHorizontalHeaderLabels(df.columns.tolist() + ['Cancel'])
        else:
            self.window3.labeln.setText("There is no upcoming bookings!")
            self.window3.labeln.setStyleSheet("color: red")
            self.window3.labeln.setGeometry(40, 114, 400, 20)

    @staticmethod
    def input_checkup(name, email, phone):
        if all([substring in email for substring in ['.', '@']]) and any(x.isalpha() for x in name) and phone[
                                                                                                        1:].isnumeric():
            return True

    def reserve(self):
        if self.checkBox.isChecked():
            self.label7.clear()
            name = self.name.text()
            email = self.email.text()
            phone = "'" + self.phone.text()
            service = self.service.currentText()
            doctor = self.doctor.currentText()
            date = '{2}-{0}-{1}'.format(self.calendar.selectedDate().month(), self.calendar.selectedDate().day(),
                                        self.calendar.selectedDate().year())
            item = self.listWidget.currentItem()
            if name is not None and email is not None and phone is not None and self.input_checkup(name, email, phone):
                if item is not None:
                    time = item.text()
                    c = Customer(name, phone, email)
                    a = c.reserve(date, time, service, doctor)
                    if a is None:
                        # self.close()
                        self.window.label.clear()
                        self.window.label.setText(
                            f"{service}:\n{time} on {date} \nwith doctor {doctor} is confirmed!\nThank you!:)")
                        font = QFont()
                        font.setPointSize(16)
                        self.window.label.setFont(font)
                        self.window.show()
                    else:
                        txt = a + ' Please choose a new time!'
                        self.label7.setText(a)

                else:
                    self.label7.setText('Please select a date and time for booking!')
                    self.label7.setStyleSheet("color: red")
            else:
                self.label7.setText('Some information is not correct or missing!')
                self.label7.setStyleSheet("color: red")
        else:
            self.label7.setText("Please confirm your booking by checking the checkbox!")
            self.label7.setStyleSheet("color: red")

    def update_combobox(self):
        for k, v in self.dic.items():
            service = QStandardItem(k)
            self.model.appendRow(service)
            for value in v:
                doctor = QStandardItem(value)
                service.appendRow(doctor)
        self.service.currentIndexChanged.connect(self.update_service)
        self.update_service(0)

    def update_service(self, index):
        index = self.model.index(index, 0, self.service.rootModelIndex())
        self.doctor.setRootModelIndex(index)
        self.doctor.setCurrentIndex(0)

    def init_calendar(self):
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate(currentYear, currentMonth, currentDay))
        self.calendar.setMaximumDate(
            QDate(currentYear, currentMonth + 1, calendar.monthrange(currentYear, currentMonth)[1]))
        self.calendar.setSelectedDate(QDate(currentYear, currentMonth, 1))
        self.calendar.clicked.connect(self.get_time)

    def get_time(self, QDate):
        doctor_name = self.doctor.currentText()
        service_name = self.service.currentText()
        duration = self.service_time[service_name]
        a = Doctor(doctor_name)
        date = '{2}-{0}-{1}'.format(QDate.month(), QDate.day(), QDate.year())
        self.listWidget.clear()
        if pd.to_datetime(date).weekday() < 5:
            if pd.to_datetime(date) > datetime.today():
                for i in a.show_available_slots(date, service_name):
                    time = (datetime.strptime(i, '%H:%M') + timedelta(minutes=duration))
                    end_time = datetime.strftime(time, '%H:%M')
                    item = i + ' - ' + end_time
                    self.listWidget.addItem(item)
            else:
                x = [datetime.strptime(i, '%H:%M') for i in a.show_available_slots(date, service_name)]
                x = [j for j in x if datetime.now().time() < j.time()]
                x = [datetime.strftime(i, '%H:%M') for i in x]
                for i in x:
                    time = (datetime.strptime(i, '%H:%M') + timedelta(minutes=duration))
                    end_time = datetime.strftime(time, '%H:%M')
                    item = i + ' - ' + end_time
                    self.listWidget.addItem(item)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ex = ReservationSystem()
    sys.exit(app.exec_())


main()
