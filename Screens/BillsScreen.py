import sqlite3
from datetime import datetime
from typing import Any
from PyQt6 import QtCore
from PyQt6.QtWidgets import  (
    QStackedWidget, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollBar, QScrollArea, QScroller,
    QMessageBox, QGraphicsGridLayout, QGridLayout, QTableWidget, QTableWidgetItem, QDateEdit,
    )
from PyQt6.QtGui import QIcon, QFont


from Database.dao import AccessDatabase
from Database.dto import ModifyDatabase
from Classes.dbClasses import Bill
from Email.reminder_emails import send_reminder_email


class BillsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label1 = QLabel("Amount")
        self.amount_input = QLineEdit()
        self.label2 = QLabel("Due Date")
        self.due_date_input = QDateEdit()
        self.label3 = QLabel("User ID")
        self.user_id_input = QLineEdit()
        self.label4 = QLabel("Details")
        self.details_input = QLineEdit()
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")

        layout.addWidget(self.label1)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.label2)
        layout.addWidget(self.due_date_input)
        layout.addWidget(self.label3)
        layout.addWidget(self.user_id_input)
        layout.addWidget(self.label4)
        layout.addWidget(self.details_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        self.add_button.clicked.connect(self.add_bill)
        self.delete_button.clicked.connect(self.delete_bill)


        self.table = QTableWidget()
        self.table.setColumnCount(5)
        
        self.table.setHorizontalHeaderLabels(["Bill ID", "Amount", "Due Date", "details", "User id"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 80)
        self.view_table()

        layout.addWidget(self.table)

        self.setLayout(layout)

        self.bills_reminder_email()



    def view_table(self):
        bills = AccessDatabase().getAllBills()
        self.table.setRowCount(0)
        self.table.setRowCount(len(bills))
        i=0
        for bill in bills:
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(bill[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(bill[1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(bill[2])))
            self.table.setItem(i, 3, QTableWidgetItem(str(bill[3])))
            self.table.setItem(i, 4, QTableWidgetItem(str(bill[4])))
            i+=1
        i=0

    def add_bill(self):
        try:
            amount = self.amount_input.text()
            due_date = self.due_date_input.text()
            due_date = due_date.replace('/', '-')
            details = self.details_input.text()
            user_id = self.user_id_input.text()

            bill = Bill(bill_id=1, amount=amount, due_date=due_date, user_id=user_id, details=details)
            ModifyDatabase().addBill(bill)
            self.view_table()
            self.show_message("Bill added successfully!")
        except:
            self.show_message("Failed to add Bill")

    def delete_bill(self):
        try:
            selected_row = self.table.currentRow()

            # Ensure a row is selected
            if selected_row >= 0:
                id_item = self.table.item(selected_row, 0)
                row_id = int(id_item.text())

                ModifyDatabase().deleteBill(row_id)
                self.table.removeRow(selected_row)
                self.show_message("Bill deleted successfully")
        except:
            self.show_message("Failed to delete Bill!")


    def bills_reminder_email(self):
        try:
            bills = AccessDatabase().getAllBills()
            for bill in bills:
                bill_id = str(bill[0])
                amount = str(bill[1])
                due_date = str(bill[2])
                details = str(bill[3])
                user_id = str(bill[4])
                date_format = "%Y-%m-%d"
                date_object = datetime.strptime(due_date, date_format).date()

                if date_object > datetime.now().date():
                    user = AccessDatabase().getUser(int(user_id))
                    recipient_email = user.email

                    subject = f"Bill reminder"
                    message = f"The due date of bill with id; {bill_id} has officially passed. Details; {details}. Please endeavour to pay your bills."
                    send_reminder_email(recipient_email=recipient_email, subject=subject, message=message)
                    self.show_message(f"Reminder email sent to {recipient_email}")
        except:
            # self.show_message("Failed to send email!")
            pass


    def show_message(self, message):
        QMessageBox.information(self, 'Message', message)
