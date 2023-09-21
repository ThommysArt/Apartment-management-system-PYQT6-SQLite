from Database import dao, dto
from Classes.dbClasses import *
import pretty_errors
from datetime import datetime
from datetime import date
import json


pretty_errors.configure(
    separator_character='#',
    filename_display=pretty_errors.FILENAME_FULL,
    lines_before=5,
    lines_after=5,
)



dto.ModifyDatabase().deleteAllData()




# Read the JSON data from the file
with open("sample_data.json", "r") as file:
    data = json.load(file)

# Parse the data and store it in variables
apartments = data["apartments"]
bills = data["bills"]
payments = data["payments"]
users = data["users"]

# Print the variables to verify the data

for apartment in apartments:
    apt = Apartment(aptNo=apartment["apartment_number"], status=apartment["status"])
    dto.ModifyDatabase().addApartment(apt)


for bill in bills:
    bill = Bill(bill_id=bill["bill_id"], amount=bill["amount"], due_date=datetime.strptime(bill["due_date"], "%Y-%m-%d").date(), user_id=bill["user_id"], details=bill["details"])
    dto.ModifyDatabase().addBill(bill)


for payment in payments:
    pyt = Payment(id=payment["payment_id"], amount=payment["amount"], date=datetime.strptime(payment["date"], "%Y-%m-%d").date(), bill_id=payment["bill_id"])
    dto.ModifyDatabase().addPayment(pyt)


for user in users:
    user = User(name=user["name"], aptNo=user["apartment_number"], debts=user["debts"], email=user["email"], user_id=user["user_id"])
    dto.ModifyDatabase().addUser(user)




'''
for i in range(20):
    pyt = Payment(id=i+1, amount=50000/(i+1), date=date(2023,4,i+1), bill_id=i+1)
    dto.ModifyDatabase().addPayment(pyt)
'''



'''
for i in range(20):
    bill = Bill(bill_id=i+1, amount=60000, due_date=date(2023,10,19), user_id=i+1, details="rent")
    dto.ModifyDatabase().addBill(bill)
'''


'''
for i in range(20):
    user = User(name = f"User{i+1}", aptNo=i+1, debts=i*50000, email=f"user{i+1}@gmail.com", user_id=i+1)
    dto.ModifyDatabase().addUser(user)
'''

'''
for i in range(20):
    apt = Apartment(aptNo=i+1, status="Occupied")
    dto.ModifyDatabase().addApartment(apt)
'''