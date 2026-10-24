# PrintSync

PrintSync is an offline, local printing shop management system built with Python and PyQt6. The application features separate user and admin screens designed for a dual-monitor setup.

## Project Structure
```text
OOP2B-Group-Project/
├── admin_screen.py
├── main.py
├── user_screen.py
└── README.md
```

## Target Features

- **Dual-Monitor Interface** – Separate user and admin screens.
- **Order Management** – Record and manage printing orders.
- **Order Summary** – Display paper sizes, quantities, printing modes, and individual prices.
- **Automatic Pricing** – Calculate costs based on paper size, quantity, and printing type.
- **File Submission Tracking** – Specify whether customers sent their files through Gmail or Facebook.
- **Customer Information** – Record the customer's name, Facebook account, email address, and phone number.
- **Offline Operation** – Designed to operate locally without requiring an internet connection for core functions.

## Technologies Used

- Python
- PyQt6

## Sample Pricing

| Item | Price |
|---|---:|
| Letter-size paper | ₱2.00 per sheet |
| Black and white printing | +₱2.00 per page |
| Colored printing | +₱3.00 per page |

*Prices are sample values and can be adjusted based on the printing shop's actual rates.*

## Purpose

This project was developed as an Object-Oriented Programming 2 group project to demonstrate GUI development, order management, and object-oriented programming concepts using Python and PyQt6.
