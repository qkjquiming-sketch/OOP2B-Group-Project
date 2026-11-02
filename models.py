from config import Statuses
from dialogs import showAlert

class Order:
    
    headerCSV = ["Order Number", "Customer Name", "Phone", "Account", "Job Details", "Source", "Amount", "Status"]
    
    def __init__(self, orderId, name, phone, account, job, source, amount, status="Pending"):
        self.id = orderId
        self.name = name
        self.phone = phone
        self.account = account
        self.job = job
        self.source = source
        self.amount = float(amount)
        self.status = "Pending"
        self.setStatus(status) 
        
    # ----- Status -----
    def setStatus(self, value):
        if value not in Statuses:
            showAlert("Invalid Status", f"Unknown Status: {value} ")
            return
        self.status = value
        
    # Rules for the orders
    def isOpen(self):   return self.status not in ("Completed", "Cancelled")    # Does not count Completed and Cancelled orders as open jobs
    def countsAsSale(self): return self.status != "Cancelled"                   # Does not count Cancelled orders in Total Sales
    
    # This makes the order["id"] work
    def __getitem__(self, key): return getattr(self, key)
    def __setitem__(self, key, value):
        if key == "status": self.setStatus(value)
        else: setattr(self, key, value)
    def get(self, key, default=""): return getattr(self, key, default)
    
    
    # Convert CSV
    def toRow(self):
        return[self.id, self.name, self.phone, self.account, self.job, self.source, self.amount, self.status]

# ----- orderFromRow -----
def orderFromRow(row):
    return Order(
    row["Order Number"],
    row["Customer Name"],
    row["Phone"],
    row["Account"],
    row["Job Details"],
    row["Source"],
    row["Amount"],
    row["Status"]
    )