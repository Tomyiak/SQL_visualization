import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton,
                             QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("Shedule")
        self.move(250, 100)  # Здесь где окно появится
        self.resize(830, 720)  # Здесь размер окна (изначальный)
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_subjects_tab()
        self.create_second_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="schedule_db",
                                     user="postgres",
                                     password="1234",
                                     host="localhost",
                                     port="5432")
        self.cursor = self.conn.cursor()

    def _create_subjects_tab(self):
        self.subjects_tab = QWidget()
        self.tabs.addTab(self.subjects_tab, "Subjects")
        self.subjects_tab_gbox = QGroupBox("Subjects")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.subjects_tab_gbox)
        self._create_all_subjects_table()
        self.update_subjects_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_subjects_button)
        self.update_subjects_button.clicked.connect(self._update_subject)
        self.subjects_tab.setLayout(self.svbox)

    def _create_all_subjects_table(self):
        self.all_subjects_table = QTableWidget()
        self.all_subjects_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.all_subjects_table.setColumnCount(7)
        self.all_subjects_table.setHorizontalHeaderLabels(
            ["day", 'subject', 'lecture_hall', 'time', 'professor', "", ""])
        self._update_subjects_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.all_subjects_table)
        self.subjects_tab_gbox.setLayout(self.mvbox)

    def _update_subjects_table(self):
        self.cursor.execute("SELECT * FROM days_table;")
        records = list(self.cursor.fetchall())
        self.all_subjects_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.all_subjects_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.all_subjects_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.all_subjects_table.setItem(i, 2, QTableWidgetItem(str(r[3])))
            self.all_subjects_table.setItem(i, 3, QTableWidgetItem(str(r[4])))
            self.all_subjects_table.setItem(i, 4, QTableWidgetItem(str(r[5])))
            self.all_subjects_table.setCellWidget(i, 5, joinButton)
            self.all_subjects_table.setCellWidget(i, 6, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r: self._change_subject(num, data))
            deleteButton.clicked.connect(lambda ch, data=r: self._delete_subject(data))
        addButton = QPushButton("Add")
        self.all_subjects_table.setCellWidget(i + 1, 5, addButton)
        addButton.clicked.connect(lambda ch, num=i + 1: self._insert_subject(num))
        self.all_subjects_table.resizeRowsToContents()

    def _delete_subject(self, data):
        try:
            self.cursor.execute(f"DELETE FROM days_table WHERE id='{data[0]}';")
            self.conn.commit()
            self._update_subjects_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields0")

    def _change_subject(self, rowNum, data):
        row = list()
        for i in range(self.all_subjects_table.columnCount()):
            try:
                row.append(self.all_subjects_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            print(data)
            print(row)
            self.cursor.execute(
                f"UPDATE days_table SET day='{row[0]}', subject='{row[1]}', lecture_hall='{row[2]}', time='{row[3]}', professor='{row[4]}' WHERE id='{data[0]}'"
            )
            self.conn.commit()
            self._update_subjects_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields1")

    def _insert_subject(self, rowNum):
        print(rowNum)
        row = list()
        for i in range(self.all_subjects_table.columnCount()):
            try:
                row.append(self.all_subjects_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(
                f"INSERT INTO days_table (day, subject, lecture_hall, time, professor) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}');"
            )
            self.conn.commit()
            self._update_subjects_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields2")

    def _update_subject(self):
        self._update_subjects_table()

    def create_second_tab(self):
        self.second_tab = QWidget()
        self.tabs.addTab(self.second_tab, "second_tab")
        self.second_tab_gbox = QGroupBox("second_tab")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.second_tab_gbox)
        self.create_all_Second_table()
        self.update_second_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_second_button)
        self.update_second_button.clicked.connect(self.update_second)
        self.second_tab.setLayout(self.svbox)

    def create_all_Second_table(self):
        self.all_Second_table = QTableWidget()
        self.all_Second_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.all_Second_table.setColumnCount(4)
        self.all_Second_table.setHorizontalHeaderLabels(["f1st", "s2nd", "", ""])
        self.update_Second_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.all_Second_table)
        self.second_tab_gbox.setLayout(self.mvbox)

    def update_Second_table(self):
        self.cursor.execute("SELECT * FROM second_tab;")
        records = list(self.cursor.fetchall())
        self.all_Second_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.all_Second_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.all_Second_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.all_Second_table.setCellWidget(i, 2, joinButton)
            self.all_Second_table.setCellWidget(i, 3, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r: self.change_second(num, data))
            deleteButton.clicked.connect(lambda ch, data=r: self.delete_second(data))
        addButton = QPushButton("Add")
        self.all_Second_table.setCellWidget(i + 1, 2, addButton)
        addButton.clicked.connect(lambda ch, num=i + 1: self.insert_second(num))
        self.all_Second_table.resizeRowsToContents()

    def delete_second(self, data):
        try:
            self.cursor.execute(f"DELETE FROM second_tab WHERE f1st='{data[0]}';")
            self.conn.commit()
            self.update_Second_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields0")

    def change_second(self, rowNum, data):
        row = list()
        for i in range(self.all_Second_table.columnCount()):
            try:
                row.append(self.all_Second_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            print(data)
            print(row)
            self.cursor.execute(f"UPDATE second_tab SET f1st='{row[0]}', s2nd='{row[1]}' WHERE f1st='{data[0]}'")
            self.conn.commit()
            self.update_Second_table()
            print(row)
        except:
            QMessageBox.about(self, "Error", "Enter all fields1")

    def insert_second(self, rowNum):
        print(rowNum)
        row = list()
        for i in range(self.all_Second_table.columnCount()):
            try:
                row.append(self.all_Second_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(
                f"INSERT INTO second_tab (f1st, s2nd) VALUES ('{row[0]}', '{row[1]}');"
            )
            self.conn.commit()
            self.update_Second_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields2")

    def update_second(self):
        self.update_Second_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
