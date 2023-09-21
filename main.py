import sqlite3
import sys
from PyQt6.QtWidgets import  (
    QStackedWidget, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QMainWindow, QGraphicsAnchorLayout
    )
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPixmap


from Screens.Dashboard import Dashboard
from Screens.BillsScreen import BillsScreen
from Screens.UsersScreen import UsersScreen
from Screens.PaymentsScreen import PaymentsScreen
from Screens.ApartmentScreen import ApartmentScreen
import pretty_errors


pretty_errors.configure(
    separator_character='#',
    filename_display=pretty_errors.FILENAME_FULL,
    lines_before=5,
    lines_after=5,
)


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        ################################################################################
        # Left Menu


        self.dashboard_button = QPushButton("Dashboard")
        self.apartment_button = QPushButton("Apartment")
        self.users_button = QPushButton("Users")
        self.payments_button = QPushButton("Payments")
        self.bills_button = QPushButton("Bills")
    

        layout = QVBoxLayout()

        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.apartment_button)
        layout.addWidget(self.users_button)
        layout.addWidget(self.payments_button)
        layout.addWidget(self.bills_button)
        self.dashboard_button.clicked.connect(self.switch_to_dashboard)
        self.apartment_button.clicked.connect(self.switch_to_apartments_screen)
        self.users_button.clicked.connect(self.switch_to_users_screen)
        self.payments_button.clicked.connect(self.switch_to_payments_screen)
        self.bills_button.clicked.connect(self.switch_to_bills_screen)

        self.setLayout(layout)

    def switch_to_dashboard(self):
        self.window().current_screen.stacked_widget.setCurrentWidget(self.window().current_screen.dashboard_screen)

    def switch_to_users_screen(self):
        self.window().current_screen.stacked_widget.setCurrentWidget(self.window().current_screen.users_screen)

    def switch_to_payments_screen(self):
        self.window().current_screen.stacked_widget.setCurrentWidget(self.window().current_screen.payment_screen)

    def switch_to_bills_screen(self):
        self.window().current_screen.stacked_widget.setCurrentWidget(self.window().current_screen.bills_screen)

    def switch_to_apartments_screen(self):
        self.window().current_screen.stacked_widget.setCurrentWidget(self.window().current_screen.apartments_screen)
    


class WindowManager(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.dashboard_screen = Dashboard()
        self.apartments_screen = ApartmentScreen()
        self.bills_screen = BillsScreen()
        self.users_screen = UsersScreen()
        self.payment_screen = PaymentsScreen()

        self.stacked_widget.addWidget(self.dashboard_screen)
        self.stacked_widget.addWidget(self.apartments_screen)
        self.stacked_widget.addWidget(self.bills_screen)
        self.stacked_widget.addWidget(self.users_screen)
        self.stacked_widget.addWidget(self.payment_screen)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)


class MainApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("APARTMENT MANAGEMENT SYSTEM")
        self.setWindowIcon(QIcon("./assets/icons8_apartment_64px.png"))
        self.setStyleSheet(open('css/style.css').read())

        layout = QHBoxLayout()
        self.menu = Menu()
        self.menu.setFixedSize(200, 600)
        self.current_screen = WindowManager()
        self.current_screen.setFixedSize(700, 600)


        layout.addWidget(self.menu)
        layout.addWidget(self.current_screen)

        self.setLayout(layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    window.resize(900, 600)
    sys.exit(app.exec())

    