import os  #NEW
import re  #NEW
import sys  #NEW
from datetime import datetime  #NEW

LOG_NAME = "orders.txt"  #NEW the history file, it is created the first time an order is placed


def log_path():  #NEW
    #NEW Next to PrintSync.exe when packaged, next to the .py files when running normally
    if getattr(sys, "frozen", False):  #NEW
        base_dir = os.path.dirname(sys.executable)  #NEW
    else:  #NEW
        base_dir = os.path.dirname(os.path.abspath(__file__))  #NEW
    return os.path.join(base_dir, LOG_NAME)  #NEW


def _append(text):  #NEW
    #NEW Returns False instead of crashing if the file cannot be written
    try:  #NEW
        with open(log_path(), "a", encoding="utf-8") as f:  #NEW
            f.write(text)  #NEW
        return True  #NEW
    except OSError:  #NEW
        return False  #NEW


def _now():  #NEW
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #NEW


def log_order(order):  #NEW
    #NEW Adds one block to orders.txt for a newly placed order
    return _append(  #NEW
        f"[{_now()}] NEW ORDER {order['id']}\n"  #NEW
        f"  Customer : {order['name']}\n"  #NEW
        f"  Phone    : {order['phone'] or 'N/A'}\n"  #NEW
        f"  Account  : {order['account'] or 'N/A'}\n"  #NEW
        f"  Source   : {order['source']}\n"  #NEW
        f"  Job      : {order['job']}\n"  #NEW
        f"  Amount   : ₱{order['amount']:.2f}\n"  #NEW
        f"  Status   : {order['status']}\n"  #NEW
        f"{'-' * 60}\n"  #NEW
    )  #NEW


def log_status(order_id, status):  #NEW
    #NEW Adds one line to orders.txt when the admin changes an order's status
    return _append(f"[{_now()}] STATUS {order_id} -> {status}\n{'-' * 60}\n")  #NEW


def last_order_number(default=1000):  #NEW
    #NEW Reads orders.txt so new order codes continue after a restart (PS-1004 comes after PS-1003)
    try:  #NEW
        with open(log_path(), "r", encoding="utf-8") as f:  #NEW
            numbers = re.findall(r"NEW ORDER PS-(\d+)", f.read())  #NEW
    except OSError:  #NEW
        return default  #NEW
    return max([int(n) for n in numbers] + [default])  #NEW