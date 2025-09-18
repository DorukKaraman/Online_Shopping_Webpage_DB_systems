# 🛒 Online Auction System (Mock Database Simulation)

This project is a **mock simulation of an online shopping/auction platform** built using **SQLite** and **PySimpleGUI**.  
It was developed as part of the *Computers and Data Organization* course to explore:  
- How **relational databases** are structured and queried.  
- The interaction between a **database backend** and a **graphical user interface (GUI)**.  
- Core concepts of **database design**, including users, auctions, bids, billing, and ownership relations.  

---

## 🔑 Features

### 👤 User Management
- Login system with **Buyer** and **Seller** roles.
- Sellers can update personal info (name, surname, IBAN, password).

### 🏷️ Seller Features
- Create new auctions with:
  - Title, description, category
  - Start and buy-it-now prices
  - End date
- View/manage ongoing auctions.
- List bidders for an auction.
- View bills and generated transactions.
- Delete auctions or finalize them.

### 💰 Buyer Features
- View all active auctions.
- Place bids on auctions.

### 📊 Billing
- Track transactions and net amounts associated with completed auctions.

---

## 🛠️ Tech Stack
- **Python 3**
- **SQLite** (Relational Database)
- **PySimpleGUI** (GUI framework)

---

## 🚀 Getting Started

### 1. Clone the Repository

### 2. Install Dependencies
- pip install PySimpleGUI

### 3. Create the database
- sqlite3 shopping_db.db < schema.sql

### 4. Run the Project
- python shopping_project.py

---

## Project Structure
.
├── cs281proje.py      # Main Python script (GUI + database logic)
├── database1.db       # SQLite database (auto-created if it does not exist)
├── schema.sql         # SQL schema to rebuild the database from scratch
└── README.md          # Project description and setup guide

