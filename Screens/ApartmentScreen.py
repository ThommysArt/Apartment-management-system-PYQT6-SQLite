
import sqlite3
from PyQt6 import QtCore
from PyQt6.QtWidgets import  (
    QStackedWidget, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollBar, QScrollArea, QScroller,
    QMessageBox, QGraphicsGridLayout, QGridLayout, QTableWidget, QTableWidgetItem
    )
from PyQt6.QtGui import QIcon, QFont


from Database.dao import AccessDatabase
from Database.dto import ModifyDatabase
from Classes.dbClasses import Apartment

class ApartmentScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.aptNo_label = QLabel("Apartment No")
        self.aptNo_input = QLineEdit()
        self.status_label = QLabel("Status")
        self.status_input = QLineEdit()
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")

        layout.addWidget(self.aptNo_label)
        layout.addWidget(self.aptNo_input)
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        self.add_button.clicked.connect(self.add_apt)
        self.delete_button.clicked.connect(self.delete_apt)
        

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 300)
        self.table.setHorizontalHeaderLabels(["Apartment No", "Status"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.view_table()

        layout.addWidget(self.table)

        self.setLayout(layout)

    def view_table(self):
        apartments = AccessDatabase().getAllApartments()
        self.table.setRowCount(0)
        self.table.setRowCount(len(apartments))
        i=0
        for apt in apartments:
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(apt[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(apt[1])))
            i+=1
        i=0

    def add_apt(self):
        try:
            aptNo = self.aptNo_input.text()
            status = self.status_input.text()

            apt = Apartment(aptNo=aptNo, status=status)
            ModifyDatabase().addApartment(apt)
            self.view_table()
            self.show_message("Apartment added successfully!")
        except:
            self.show_message("Failed to add Apartment!")

    def delete_apt(self):
        try:
            selected_row = self.table.currentRow()

            # Ensure a row is selected
            if selected_row >= 0:
                id_item = self.table.item(selected_row, 0)
                row_id = int(id_item.text())

                ModifyDatabase().deleteApartment(row_id)
                self.table.removeRow(selected_row)
                self.show_message("Apartment deleted successfully")
        except:
            self.show_message("Failed to delete Apartment")

    def show_message(self, message):
        QMessageBox.information(self, 'Message', message)



