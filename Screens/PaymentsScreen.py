import sqlite3
from typing import Any
from PyQt6 import QtCore
from PyQt6.QtWidgets import  (
    QStackedWidget, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollBar, QScrollArea, QScroller,
    QMessageBox, QGraphicsGridLayout, QGridLayout, QTableWidget, QTableWidgetItem, QDateEdit
    )
from PyQt6.QtGui import QIcon, QFont


from Database.dao import AccessDatabase
from Database.dto import ModifyDatabase
from Classes.dbClasses import Payment


class PaymentsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label1 = QLabel("Amount")
        self.amount_input = QLineEdit()
        self.label2 = QLabel("Date")
        self.date_input = QDateEdit()
        self.label3 = QLabel("Bill_id")
        self.bill_id_input = QLineEdit()
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")

        layout.addWidget(self.label1)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.label2)
        layout.addWidget(self.date_input)
        layout.addWidget(self.label3)
        layout.addWidget(self.bill_id_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        self.add_button.clicked.connect(self.add_payment)
        self.delete_button.clicked.connect(self.delete_payment)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 200)
        self.table.setHorizontalHeaderLabels(["ID", "Amount", "Date", "Bill id"])
        self.view_table()

        layout.addWidget(self.table)

        self.setLayout(layout)

    def view_table(self):
        payments = AccessDatabase().getAllPayments()
        self.table.setRowCount(0)
        self.table.setRowCount(len(payments))
        i=0
        for payment in payments:
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(payment[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(payment[1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(payment[2])))
            self.table.setItem(i, 3, QTableWidgetItem(str(payment[3])))
            i+=1
        i=0

    def add_payment(self):
        try:
            amount = self.amount_input.text()
            date = self.date_input.text()
            bill_id = self.bill_id_input.text()

            pyt = Payment(id=1, amount=amount, date=date, bill_id=bill_id)
            ModifyDatabase.addPayment(pyt)
            self.view_table()
            self.show_message("Apartment added successfully!")
        except:
            self.show_message("Failed to add payment!")

    def delete_payment(self):
        try:
            selected_row = self.table.currentRow()

            # Ensure a row is selected
            if selected_row >= 0:
                id_item = self.table.item(selected_row, 0)
                row_id = int(id_item.text())

                ModifyDatabase().deletePayment(row_id)
                self.table.removeRow(selected_row)
                self.show_message("Apartment added successfully!")
        except:
            self.show_message("Failed to delete Apartment!")

        

    def show_message(self, message):
        QMessageBox.information(self, 'Message', message)