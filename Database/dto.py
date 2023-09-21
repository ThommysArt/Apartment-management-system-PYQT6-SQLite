import sqlite3
from Classes.dbClasses import *

class ModifyDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("Database/database.db")
        self.cursor = self.conn.cursor()
 
    ################################################################################################################################################################################
    # ADDING NEW DATA SETS
    def addUser(self, user: User):
        self.cursor.execute("INSERT INTO User (name, aptNo, debts, email) VALUES (?, ?, ?, ?)", (user.name, user.aptNo, user.debts, user.email))
        self.conn.commit()

    def addPayment(self, payment: Payment):
        self.cursor.execute("INSERT INTO Payments (amount, date, bill_id) VALUES (? , ?, ?)", (payment.amount, payment.date, payment.bill_id))
        self.conn.commit()

    def addBill(self, bill: Bill):
        self.cursor.execute("INSERT INTO Bill (amount, due_date, user_id, details) VALUES (?, ?, ?, ?)", (bill.amount, bill.due_date, bill.user_id, bill.details))
        self.conn.commit()

    def addApartment(self, apartment: Apartment):
        self.cursor.execute("INSERT INTO Apartment (aptNo, status) VALUES (? ,?)", (apartment.aptNo, apartment.status))
        self.conn.commit()


    ###########################################################################################################################################################################################
    # UPDATING DATA SETS
    def setUser(self, user: User):
        self.cursor.execute(f"UPDATE User SET aptNo = {user.aptNo}, debts = {user.debts}, email = {user.email} WHERE user_id = ?", (user.user_id))
        self.conn.commit()

    def setPayment(self, payment: Payment):
        self.cursor.execute(f"UPDATE Payments SET amount = {payment.amount}, date = {payment.date}, bill_id = {payment.bill_id} WHERE id = ?", (payment.id))
        self.conn.commit()

    def setBill(self, bill: Bill):
        self.cursor.execute(f"UPDATE Bills SET details = {bill.details}, amount = {bill.amount}, due_date = {bill.due_date}, bill_id = {bill.user_id} WHERE user_id = ?", (bill.bill_id))
        self.conn.commit()

    def setApartment(self, apartment: Apartment):
        self.cursor.execute(f"UPDATE Apartments SET aptNo = {apartment.aptNo}, status = {apartment.status} WHERE user_id = ?", (apartment.aptNo))
        self.conn.commit()


    ###################################################################################################################################################################
    # DELETE DATA

    def deleteUser(self, user_id):
        self.cursor.execute("DELETE FROM User WHERE user_id=?", (user_id,))
        self.conn.commit()

    def deletePayment(self, id):
        self.cursor.execute("DELETE FROM Payments WHERE id=?", (id,))
        self.conn.commit()

    def deleteBill(self, bill_id):
        self.cursor.execute("DELETE FROM Bill WHERE bill_id=?", (bill_id,))
        self.conn.commit()
    
    def deleteApartment(self, aptNo):
        self.cursor.execute("DELETE FROM Apartment WHERE aptNo=?", (aptNo,))
        self.conn.commit()

    def deleteAllData(self):
        # Disable foreign key constraints if enabled
        self.cursor.execute("PRAGMA foreign_keys = OFF")

        # Retrieve a list of table names in the database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()

        # Clear data from each table
        for table in tables:
            table_name = table[0]
            self.cursor.execute(f"DELETE FROM {table_name};")
            print(f"Data cleared from table: {table_name}")

        self.conn.commit()

        self.cursor.execute("PRAGMA foreign_keys = ON")

        self.cursor.execute("VACUUM;")

        self.conn.close()