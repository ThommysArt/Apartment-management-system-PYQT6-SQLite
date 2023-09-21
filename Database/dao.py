import sqlite3
from Classes.dbClasses import *


class AccessDatabase():
    def __init__(self):
        self.conn = sqlite3.connect("Database/database.db")
        self.cursor = self.conn.cursor()
        # self.create_tables()

    ###########################################################################################################################################################
    # CREATE DATA TABLES
    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS User(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    debts INTEGER DEFAULT 0,
                    aptNo INTEGER,
                    FOREIGN KEY(aptNo) REFERENCES Apartment(aptNo)              
                        )
                ''')
            print("user table created successfully")
        except:
            print("failed to create user table")

        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Bill(
                    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount INTEGER NOT NULL,
                    due_date REAL NOT NULL,
                    details VARCHAR(100) NOT NULL,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES User(user_id)
                    )
                ''')
            print("Bill table created successfully")
        except:
            print("failed to create Bill table")

        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Payments(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount INTEGER NOT NULL,
                    date REAL NOT NULL,
                    bill_id INTEGER,
                    FOREIGN KEY(bill_id) REFERENCES Bill(bill_id)
                    )
                ''')
            print("Payments table created successfully")
        except:
            print("failed to create Payments table")

        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Apartment(
                    aptNo INTEGER PRIMARY KEY AUTOINCREMENT,
                    status VARCHAR(20) NOT NULL
                    )
                ''')
            print("Apartment table created successfully")
        except:
            print("failed to create Apartment table")


    ############################################################################################################################################################
    # GETTERS
    def getUser(self, id):
        self.cursor.execute(" SELECT aptNo FROM User WHERE user_id = ?",(id,))
        aptNo = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT debts FROM User WHERE user_id = ?", (id,))
        debts = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT email FROM User WHERE user_id = ?", (id,))
        email = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT name FROM User WHERE user_id = ?", (id,))
        name = self.cursor.fetchone()[0]

        user = User(user_id=id, name=name, aptNo=aptNo, debts=debts, email=email)
        return user

    def getBill(self, id):
        self.cursor.execute(" SELECT amount FROM Bill WHERE bill_id = ?", (id,))
        amount = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT due_date FROM Bill WHERE bill_id = ?", (id,))
        due_date = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT user_id FROM Bill WHERE bill_id = ?", (id,))
        user_id = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT details FROM Bill WHERE bill_id = ?", (id,))
        details = self.cursor.fetchone()[0]

        bill = Bill(bill_id=id, amount=amount, due_date=due_date, user_id=user_id, details=details)
        return bill

    def getPayments(self, id):
        self.cursor.execute(" SELECT amount FROM Payments WHERE id = ?", (id,))
        amount = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT date FROM Payments WHERE id = ?", (id,))
        date = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT bill_id FROM Payments WHERE id = ?", (id,))
        bill_id = self.cursor.fetchone()[0]

        payment = Payment(id=id, amount=amount, date=date, bill_id=bill_id)
        return payment
    

    def getApartment(self, id):
        self.cursor.execute(" SELECT status FROM Apartment WHERE aptNo = ?", (id,))
        status = self.cursor.fetchone()[0]
        

    def getAllUsers(self):
        self.cursor.execute("SELECT * FROM User")
        all_users = self.cursor.fetchall()
        return all_users

    def getAllApartments(self):
        self.cursor.execute("SELECT * FROM Apartment")
        all_apts = self.cursor.fetchall()
        return all_apts
    
    def getAllBills(self):
        self.cursor.execute("SELECT * FROM Bill")
        all_bills = self.cursor.fetchall()
        return all_bills
    
    def getAllPayments(self):
        self.cursor.execute("SELECT * FROM Payments")
        all_payments = self.cursor.fetchall()
        return all_payments
    

    def getAllBillAmounts(self):
        self.cursor.execute("SELECT amount FROM Bill")
        all_amounts = self.cursor.fetchall()
        return all_amounts

    def getAllPaymentAmounts(self):
        self.cursor.execute("SELECT amount FROM Payments")
        all_amounts = self.cursor.fetchall()
        return all_amounts
    
    def getAllUsersDebts(self):
        self.cursor.execute("SELECT debts FROM User")
        all_debts = self.cursor.fetchall()
        return all_debts
    
    def getAllUserBills(self, user_id):
        self.cursor.execute("SELECT * FROM Bill WHERE user_id = ?", (user_id,))
        all_user_bills = self.cursor.fetchall()
        return all_user_bills
    
    def getAllUserPayments(self, bill_id):
        self.cursor.execute("SELECT * FROM Payments WHERE bill_id = ?", (bill_id,))
        all_user_payments = self.cursor.fetchall()
        return all_user_payments
