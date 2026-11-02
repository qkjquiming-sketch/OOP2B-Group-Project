import os 
import re  
import sys  
from datetime import datetime

LOG_NAME = "orders.txt"  


def log_path(): 
   
    if getattr(sys, "frozen", False): 
        base_dir = os.path.dirname(sys.executable)
    else: 
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, LOG_NAME) 


def _append(text):  
   
    try: 
        with open(log_path(), "a", encoding="utf-8") as f: 
            f.write(text)  
        return True 
    except OSError:
        return False 


def _now(): 
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  


def log_order(order): 
  
    return _append(  
        f"[{_now()}] NEW ORDER {order['id']}\n" 
        f"  Customer : {order['name']}\n"
        f"  Phone    : {order['phone'] or 'N/A'}\n"
        f"  Account  : {order['account'] or 'N/A'}\n"
        f"  Source   : {order['source']}\n" 
        f"  Job      : {order['job']}\n" 
        f"  Amount   : ₱{order['amount']:.2f}\n" 
        f"  Status   : {order['status']}\n" 
        f"{'-' * 60}\n"  
    ) 


def log_status(order_id, status):
  
    return _append(f"[{_now()}] STATUS {order_id} -> {status}\n{'-' * 60}\n") 


def last_order_number(default=1000):
    
    try:  
        with open(log_path(), "r", encoding="utf-8") as f: 
            numbers = re.findall(r"NEW ORDER PS-(\d+)", f.read())
    except OSError: 
        return default
    return max([int(n) for n in numbers] + [default])
