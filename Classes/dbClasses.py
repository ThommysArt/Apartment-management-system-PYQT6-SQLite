
class User:
    def __init__(self, user_id, name, aptNo, debts, email):
        self.user_id = user_id
        self.name = name
        self.aptNo = aptNo
        self.debts = debts
        self.email = email


class Bill:
    def __init__(self, bill_id, amount, due_date, user_id, details):
        self.bill_id = bill_id
        self.amount = amount
        self.due_date = due_date
        self.user_id = user_id
        self.details = details


class Payment:
    def __init__(self, id, amount, date, bill_id):
        self.id = id
        self.amount = amount
        self.date = date
        self.bill_id = bill_id


class Apartment:
    def __init__(self, aptNo, status):
        self.aptNo = aptNo
        self.status = status