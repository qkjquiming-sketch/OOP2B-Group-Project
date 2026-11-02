import os

# General Config         

# prices Config
Prices = [
    ("Letter / Short and A4 paper per page", 2),    # Default : 2
    ("Legal / Long paper per page", 3),             # Default : 3
    ("Photo Paper per page", 25),                   # Default : 25
    ("Black and White print per page", 2),          # Default : 2
    ("Full Color print per page", 3),               # Default : 3
    ("Binding", 30),                                # Default : 30
    ("Lamination", 15),                             # Default : 15
]

pricesFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prices.json")

try:
    with open(pricesFile, "r") as file:
        saved = file.read().split()
    Prices = [(label, int(saved[i])) for i, (label, value) in enumerate(Prices)]
except Exception:
    pass

# Status
Statuses = [
    "Pending",
    "Printing",
    "Ready for Pickup",
    "Completed",
    "Cancelled",
]