import sqlite3
from typing import Any
from PyQt6 import QtCore
from PyQt6.QtWidgets import  (
    QStackedWidget, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollBar, QScrollArea, QScroller,
    QMessageBox, QGraphicsGridLayout, QGridLayout, QTableWidget, QTableWidgetItem
    )
from PyQt6.QtGui import QIcon, QFont


from Database.dao import AccessDatabase
from Database.dto import ModifyDatabase
from Classes.dbClasses import User,Bill

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sqlite3
from datetime import datetime


class UsersScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.email_label = QLabel("Email")
        self.email_input = QLineEdit()
        self.debts_label = QLabel("Debts")
        self.debts_input = QLineEdit()
        self.apt_label = QLabel("Apartment No")
        self.apt_input = QLineEdit()
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")
        self.graph_button1 = QPushButton("Plot User Bills")
        self.graph_button2 = QPushButton("Plot User Payments")

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.apt_label)
        layout.addWidget(self.apt_input)
        layout.addWidget(self.debts_label)
        layout.addWidget(self.debts_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.graph_button1)
        layout.addWidget(self.graph_button2)
        self.add_button.clicked.connect(self.add_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.graph_button1.clicked.connect(self.plot_graphs1)
        self.graph_button2.clicked.connect(self.plot_graphs2)
        


        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["User ID", "Name", "Email", "Debts", "Apartment No"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 180)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 80)
        self.view_table()

        layout.addWidget(self.table)

        self.setLayout(layout)

    def view_table(self):
        users = AccessDatabase().getAllUsers()
        self.table.setRowCount(0)
        self.table.setRowCount(len(users))
        i=0
        for user in users:
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(user[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(user[1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(user[2])))
            self.table.setItem(i, 3, QTableWidgetItem(str(user[3])))
            self.table.setItem(i, 4, QTableWidgetItem(str(user[4])))
            i+=1
        i=0


    def add_user(self):
        name = self.name_input.text()
        email = self.email_input.text()
        aptNo = self.apt_input.text()
        debts = self.debts_input.text()

        user = User(user_id=1, name=name, email=email, aptNo=aptNo, debts=debts)
        ModifyDatabase().addUser(user)
        self.view_table()


    def delete_user(self):
        selected_row = self.table.currentRow()

        # Ensure a row is selected
        if selected_row >= 0:
            id_item = self.table.item(selected_row, 0)
            row_id = int(id_item.text())

            ModifyDatabase().deleteUser(row_id)
            self.table.removeRow(selected_row)


    def plot_graphs1(self):
        selected_row = self.table.currentRow()

        # Ensure a row is selected
        if selected_row >= 0:
            id_item = self.table.item(selected_row, 0)
            row_id = int(id_item.text())
            user_bills = AccessDatabase().getAllUserBills(user_id=int(row_id))
            amounts = [row[1] for row in user_bills]
            due_dates = [row[2] for row in user_bills]

        # Plot the graph
        plt.plot(amounts, due_dates)
        plt.xlabel("Amounts")
        plt.ylabel("Dates")
        plt.title("User Bills")
        plt.grid(True)
        plt.show()

    def plot_graphs2(self):
        selected_row = self.table.currentRow()

        # Ensure a row is selected
        if selected_row >= 0:
            id_item = self.table.item(selected_row, 0)
            row_id = int(id_item.text())
            user_bills = AccessDatabase().getAllUserBills(user_id=int(row_id))
            amounts = []
            dates = []
            for bill in user_bills:
                bill_id = bill[0]
                user_payments = AccessDatabase().getAllUserPayments(bill_id=int(bill_id))
                amts = [row[1] for row in user_payments]
                dts = [row[2] for row in user_payments]
                amounts.extend(amts)
                dates.extend(dts)

        plt.plot(amounts, dates)
        plt.xlabel("Amounts")
        plt.ylabel("Dates")
        plt.title("User Payments")
        plt.grid(True)
        plt.show()



    def check_payment_extension(self, user_id):
        all_user_bills = AccessDatabase().getAllUserBills(user_id=user_id)

        for user_bill in all_user_bills:
            bill_id = str(user_bill[0])
            amount = str(user_bill[1])
            due_date = str(user_bill[2])
            details = str(user_bill[3])

            bill = Bill(bill_id=bill_id, amount=amount,due_date=due_date, details=details)


    def show_message(self, message):
        QMessageBox.information(self, 'Message', message)





    