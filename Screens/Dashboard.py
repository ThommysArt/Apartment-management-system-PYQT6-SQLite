

from PyQt6 import QtCore
from PyQt6.QtWidgets import  (
    QStackedWidget, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollBar, QScrollArea, QScroller,
    QMessageBox, QGraphicsGridLayout, QGridLayout, QTableWidget, QTableWidgetItem
    )
from PyQt6.QtGui import QIcon, QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


from Database.dao import AccessDatabase

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)

        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)

        self.figure3 = Figure()
        self.canvas3 = FigureCanvas(self.figure3)

        layout.addWidget(self.canvas1)
        layout.addWidget(self.canvas2)
        layout.addWidget(self.canvas3)
        self.setLayout(layout)
        self.plot_bill_amounts()
        self.plot_payment_amounts()
        self.plot_users_debts()
        
    
    def plot_bill_amounts(self):
        self.figure1.clear()

        all_amounts = AccessDatabase().getAllBillAmounts()

        amounts = [row[0] for row in all_amounts]

        ax = self.figure1.add_subplot(111)
        ax.hist(amounts, bins=10, edgecolor='black')
        ax.set_xlabel('Amount')
        ax.set_ylabel('Frequency')
        ax.set_title('Total bills')

        self.canvas1.draw()


    def plot_payment_amounts(self):
        self.figure2.clear()

        all_amounts = AccessDatabase().getAllPaymentAmounts()

        amounts = [row[0] for row in all_amounts]

        ax = self.figure2.add_subplot(111)
        ax.hist(amounts, bins=10, edgecolor='black')
        ax.set_xlabel('Amount')
        ax.set_ylabel('Frequency')
        ax.set_title('Total Payments')

        self.canvas2.draw()

    def plot_users_debts(self):
        self.figure3.clear()

        all_debts = AccessDatabase().getAllUsersDebts()

        debts = [row[0] for row in all_debts]

        ax = self.figure3.add_subplot(111)
        ax.hist(debts, bins=10, edgecolor='black')
        ax.set_xlabel('Debts')
        ax.set_ylabel('Frequency')
        ax.set_title('Total Debts')

        self.canvas3.draw()



