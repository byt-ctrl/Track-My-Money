
# 💰 Track My Money

The **Track My Money** is a `desktop application` designed to help users track expenses and manage budgets effortlessly . Developed with **`Python (Tkinter)`** and **`SQLite`** , it provides a user-friendly `Graphical User Interface (GUI) ` for financial management. Users can `add, remove, and view expenses` , set monthly budgets, visualize spending through `graphs and charts` , and even import expenses from `CSV files` for easy data entry.  

## 🗂️ Files Included  

- **📜 expense_tracker.py** – The **main script** that powers the application, handling **expense entry, budget tracking, and visualization**.  
- **📜 tracker.sql** – This **SQL file initializes the database** by creating necessary tables and ensuring data integrity.  
- **📂 tracker.db** – The **SQLite database file** where all expenses, categories, and budget data are stored. It is generated automatically when the program is first executed.  

## 📊 Database Structure  

The application uses an **SQLite database** with the following tables:  

- **📝 expenses** – Stores all expense records with **ID, date, amount, category, and description**, ensuring valid financial tracking.  
- **📂 categories** – Manages unique **expense categories** to keep spending organized.  
- **💲 budgets** – Holds **monthly budget data**, preventing negative budget values.  
- **📊 category_budget** – Allows setting **custom budgets** for specific expense categories.  

## 🖥️ Features  

- **📌 Add, delete, and manage expenses** through a **simple and efficient GUI**.  
- **📅 Set and track monthly budgets** with automatic balance calculations.  
- **📊 Generate insightful graphs** (Pie, Bar, and Line charts) to **analyze spending patterns**.  
- **📁 Import expenses from CSV files** for bulk entry.  
- **🚦 Budget alerts**:  
  - **🟢 Green** → Within budget  
  - **🟠 Orange** → Low balance warning  
  - **🔴 Red** → Over budget alert  

## 🎯 How It Works  

1. **Run `expense_tracker.py`** to launch the application.  
2. **Set a budget** for the month.  
3. **Enter expense details** (date, amount, category, description) and **save them**.  
4. **View and manage expenses** in a structured table.  
5. **Analyze spending trends** through **graphs and real-time budget updates**.  

This tracker is a **lightweight, efficient, and user-friendly tool** for **personal finance management**. 🏦✨  

## ⚙️ Installation  

Make sure you have **Python installed** and then install the required dependencies:  

```
pip install sqlite3 matplotlib tkinter csv  
```

---


## 🤝 Contributing:

If u have any idea's feel free to contribute   
Fork the repository if needed , make your changes, and submit a pull request.


## 📜 License:

This project is licensed under the **Apache 2.0 License**.
