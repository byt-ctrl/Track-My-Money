# WRITTEN BY OM [byt-ctrl]
# Personal Expense Tracker


""" The program uses sqlite3 for database interaction functions.
The GUI components used in this application are available through tkinter module.
The program imports tkinter components ttk, messagebox and filedialog for its advanced widgets and file dialogs.
In this project we will use matplotlib.pyplot as plt for creating graphs and charts needed for visualizations.
The from datetime import date, datetime statement enables date management for expense tracking functions and budget operations.
The program uses csv modules to deal with CSV files that serve as expense data repositories. """

import csv
import sqlite3
from datetime import date,datetime
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, messagebox,filedialog



# Initialize the database
def initialize_database() :

    """
    It is possible to access the SQLite database and execute schema on an SQL file using connect().
    Makes certain that all tables specified are created.
    """

    connection=sqlite3.connect('tracker.db')
    cursor=connection.cursor()
    with open('tracker.sql','r') as sql_file :
        cursor.executescript(sql_file.read())
    connection.commit()
    connection.close()

# Add a new expense to the database

def add_new_expense() :

    """
    Provide an Expense Record to the database.
    Checks the presence of required fields, and the form of the date or amount.
    """
    expense_date=set_date_input_button.get()
    expense_amount=set_amount_button.get()
    expense_category=set_category_input_button.get()
    expense_description=set_description_input_button.get()

    if not (expense_date and expense_amount and expense_category) :
        messagebox.showerror("Input Error","Please fill out all required fields!")
        return


    try :
        # Validate the date format
        datetime.strptime(expense_date,"%Y-%m-%d")
        # Convert amount to a float
        expense_amount=float(expense_amount)

        connection=sqlite3.connect('tracker.db')
        cursor=connection.cursor()
        cursor.execute("INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)",
                    (expense_date, expense_amount, expense_category, expense_description))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success","Expense added successfully!")
        clear_input_fields()
        display_expenses()

    except ValueError :
        messagebox.showerror("Input Error","Please ensure the date and amount are valid !")

# Set or update the budget for a specific month
def set_monthly_budget() :

    """ 
    It sets or updates budget for specific month in the database.
    Ensures mandatory fields and checks the format of the budget amount.
    """
    budget_month=month_input.get()
    budget_amount=budget_inputter.get()

    if not (budget_month and budget_amount) :
        messagebox.showerror("Input Error","Please fill out both fields!")
        return

    try:
        # Convert the budget to a float
        budget_amount=float(budget_amount)

        connection=sqlite3.connect('tracker.db')
        cursor=connection.cursor()
        cursor.execute("REPLACE INTO budgets (month , budget) VALUES (? , ?)",(budget_month, budget_amount))
        connection.commit()
        connection.close() 

        messagebox.showinfo("Success",f"Budget for {budget_month} set to ₹{budget_amount:.2f} !")
        update_budget_summary()
    except ValueError :
        messagebox.showerror("Input Error","Budget must be a valid number!")



# Delete the selected expense

def delete_selected_expense() :

    """
    The database will remove the chosen expense record.
    The program will only let users try to delete rows when a row is currently selected.
    """

    selected_row=set_expense_table.selection()
    if not selected_row :
        messagebox.showwarning("Selection Error","Please select an expense to delete!")
        return

    expense_id=set_expense_table.item(selected_row[0],"values")[0]
    connection=sqlite3.connect('tracker.db')
    cursor=connection.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?",(expense_id,))
    connection.commit()
    connection.close()

    messagebox.showinfo("Success","Expense deleted successfully!")
    display_expenses()

# Clear all input fields

def clear_input_fields() :

    """
    Reset all the input fields to their default settings.
    """

    set_date_input_button.delete(0,END)
    set_date_input_button.insert(0,date.today().strftime("%Y-%m-%d"))
    month_input.delete(0,END)
    month_input.insert(0,date.today().strftime("%Y-%m"))
    budget_inputter.delete(0,END)
    set_amount_button.delete(0,END)
    set_category_input_button.delete(0,END)
    set_description_input_button.delete(0,END)



# Display all expenses in the table
def display_expenses() :

    """
    The program retrieves all expense records from the database to show them on the table display.
    """

    connection=sqlite3.connect('tracker.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    expense_records=cursor.fetchall()
    connection.close()

    # Clear the table
    for row in set_expense_table.get_children() :
        set_expense_table.delete(row)
    # Populate the table with new data
    for record in expense_records:
        set_expense_table.insert("",END,values=record)


    update_budget_summary()

# Update the budget summary
def update_budget_summary() :

    """
    The application computes current month budget utilization metrics then updates them for the current period.
    The application shows alerts when the budget crosses set thresholds or approaches those limits.
    """
    connection=sqlite3.connect('tracker.db')
    cursor=connection.cursor()

    current_month=date.today().strftime("%Y-%m")
    cursor.execute("SELECT budget FROM budgets WHERE month = ?",(current_month,))
    monthly_budget=cursor.fetchone()
    monthly_budget=monthly_budget[0]  if monthly_budget else 0

    cursor.execute("SELECT SUM (amount) FROM expenses WHERE strftime('%Y-%m', date) = ?",(current_month,))
    total_expenses=cursor.fetchone()[0] or 0
    connection.close()

    # Update the labels
    total_expenses_label.config(text=f"Total Spent : ₹{total_expenses:.2f}")
    remaining_budget=monthly_budget-total_expenses

    # Update the remaining budget label with appropriate color coding
 
    if remaining_budget<0 :
        remaining_budget_label.config(text=f"Remaining Budget : Overdraft ₹ {-remaining_budget:.2f}",fg="red")
    elif remaining_budget<monthly_budget*0.2 :
        remaining_budget_label.config(text=f"Remaining Budget : ₹{remaining_budget:.2f}",fg="orange")
    else :
        remaining_budget_label.config(text=f"Remaining Budget : ₹{remaining_budget:.2f}",fg="green")


# Plot a graph based on user selection
def plot_expense_graph(graph_type) :

    """
    Create a graphical depiction of expenditures in the chosen type of graph (Pie, Bar, or Line) .     
    """

    connection=sqlite3.connect('tracker.db')
    cursor=connection.cursor()
    cursor.execute(" SELECT category , SUM (amount) FROM expenses GROUP BY category ")
    category_data=cursor.fetchall()
    connection.close()


    if not category_data :
        messagebox.showwarning("No Data","No expenses available to plot!")
        return
    

    categories=[row[0] for row in category_data]
    amounts=[row[1] for row in category_data]


    if graph_type == "Pie" :
        plt.pie(amounts,labels=categories,autopct='%1.1f%%',colors=["red","blue","green","yellow"])
        plt.title(' Expense Distribution by Category ')
    elif graph_type == "Bar" :
        plt.bar(categories,amounts,color=["red","blue","green","yellow"])
        plt.xlabel(' Category ')
        plt.ylabel(' Amount ')
        plt.title(' Expense Distribution by Category ')
    elif graph_type == "Line" :
        plt.plot(categories,amounts,marker='o',color="red")
        plt.xlabel(' Category ')
        plt.ylabel(' Amount ')
        plt.title(' Expense Distribution by Category ')

    plt.show()



# Import expenses from a CSV file
def import_expenses_from_csv() :

    """
    The program enables users to import expense data from any chosen CSV file.
    """
    
    file_path=filedialog.askopenfilename(filetypes=[("CSV Files","*.csv")])
    if not file_path :
        return


    try :
        with open(file_path, newline='') as csvfile:
            csv_reader=csv.reader(csvfile)
            next(csv_reader)                    # Skip header row
            connection=sqlite3.connect('tracker.db')
            cursor=connection.cursor()
            for row in csv_reader :
                cursor.execute("Insert Into expenses (date , amount , category , description) VALUES (? , ? , ? , ?)",
                               (row[0],float(row[1]),row[2],row[3]))
            connection.commit()
            connection.close()


        messagebox.showinfo("Success","Expenses imported successfully!")
        display_expenses()
    except Exception as error :
        messagebox.showerror("Import Error",f"An error occurred: {error}")



""" The Personal Expense Tracker software operates through SQLite and tkinter to enable users 
to handle budgets and record expenses for graphical financial reporting. 
This program makes financial management more effective through its basic design. """



# Initialize the Tkinter (For GUI)
initialize_database()
root=Tk()
root.title("Personal Expense Tracker")
root.geometry("800x600")
root.configure(bg="white")

frame=Frame(root,bg="white",padx=11,pady=11)  # Background GUI
frame.pack(fill=BOTH,expand=True)

# Budget Input Fields
Label(frame,text="Set Monthly Budget [Default --> Current Month]",bg="white").grid(row=0,column=0,sticky=W,pady=7) #GUI
month_input=Entry(frame,width=17)#GUI
month_input.grid(row=0,column=1,pady=7)#GUI
month_input.insert(0,date.today().strftime("%Y-%m"))

Label(frame,text="Budget Amount (₹) --> ", bg="white").grid(row=1,column=0,sticky=W,pady=7)#GUI
budget_inputter=Entry(frame,width=17)#GUI
budget_inputter.grid(row=1,column=1,pady=7)#GUI

set_budget_button=Button(frame,text="Set Budget",command=set_monthly_budget,bg="light blue",fg="black")#GUI
set_budget_button.grid(row=1,column=2,pady=7,padx=7)#GUI

# Input Fields for Expenses
Label(frame,text="Date (YYYY-MM-DD) [Default Current Date] --> ",bg="white").grid(row=2,column=0,sticky=W,pady=7)#GUI
set_date_input_button=Entry(frame,width=17)#GUI
set_date_input_button.grid(row=2,column=1,pady=7)#GUI
set_date_input_button.insert(0,date.today().strftime("%Y-%m-%d"))

Label(frame,text="Amount (₹) --> ",bg="white").grid(row=3,column=0,sticky=W,pady=7)#GUI
set_amount_button=Entry(frame,width=17)#GUI
set_amount_button.grid(row=3,column=1,pady=7)#GUI

Label(frame,text="Category --> ",bg="white").grid(row=4,column=0,sticky=W,pady=7)#GUI
set_category_input_button=Entry(frame,width=17)#GUI
set_category_input_button.grid(row=4,column=1,pady=7)#GUI

Label(frame,text="Description --> ",bg="white").grid(row=7,column=0,sticky=W,pady=7)#GUI
set_description_input_button=Entry(frame,width=17)#GUI
set_description_input_button.grid(row=7,column=1,pady=7)#GUI

# Buttons for Expense Management
set_button_frame_button=Frame(frame,bg="white")#GUI
set_button_frame_button.grid(row=6,column=0,columnspan=3,pady=11)#GUI

set_add_button=Button(set_button_frame_button,text="Add Expense",command=add_new_expense,bg="green",fg="white",width=17)#GUI
set_add_button.grid(row=0,column=0,padx=7)#GUI

set_clear_button=Button(set_button_frame_button,text="Clear Fields",command=clear_input_fields,bg="orange",fg="white",width=17)#GUI
set_clear_button.grid(row=0,column=1,padx=7)#GUI

set_delete_button=Button(set_button_frame_button,text="Delete Expense",command=delete_selected_expense,bg="red",fg="white",width=17)#GUI
set_delete_button.grid(row=0,column=2,padx=7)#GUI

set_import_button=Button(set_button_frame_button, text="Import CSV",command=import_expenses_from_csv,bg="blue",fg="white",width=17)#GUI
set_import_button.grid(row=1,column=0,pady=7,padx=7)#GUI

set_view_button=Button(set_button_frame_button,text="View Expenses",command=display_expenses,bg="gray",fg="white",width=17)#GUI
set_view_button.grid(row=1,column=1,pady=7,padx=7)#GUI



# Dropdown for Graph Options

graph_type=StringVar(value="Pie")
Label(frame,text="Select Graph Type :",bg="white").grid(row=7,column=0,sticky=W,pady=7)#GUI
graph_menu=ttk.Combobox(frame,textvariable=graph_type,values=["Pie","Bar","Line"],width=13)#GUI
graph_menu.grid(row=7,column=1,pady=7)#GUI

plotting_button=Button(frame,text="Plot Graph",command=lambda:plot_expense_graph(graph_type.get()),bg="purple",fg="white",width=17)#GUI
plotting_button.grid(row=7,column=2,pady=7)#GUI

# Budget Summary Labels
total_expenses_label=Label(root,text="Total Spent --> ₹0.00",bg="white",font=("Arial",13,"bold"))#GUI
total_expenses_label.pack(anchor=W,padx=11,pady=7)#GUI

remaining_budget_label=Label(root,text="Remaining Budget --> ₹0.00",bg="white",font=("Arial",13,"bold"))#GUI
remaining_budget_label.pack(anchor=W,padx=11,pady=7)#GUI

# Expense Table
seting_table_frame=Frame(root,bg="white",pady=11)#GUI
seting_table_frame.pack(fill=BOTH,expand=True)#GUI

set_expense_table=ttk.Treeview(seting_table_frame,columns=("ID","Date","Amount","Category","Description"),show="headings")
set_expense_table.heading("ID",text="ID")
set_expense_table.heading("Date",text="Date")
set_expense_table.heading("Amount",text="Amount")
set_expense_table.heading("Category",text="Category")
set_expense_table.heading("Description",text="Description")

set_expense_table.column("ID",width=50,anchor=CENTER)
set_expense_table.column("Date",width=100,anchor=W)
set_expense_table.column("Amount",width=100,anchor=W)
set_expense_table.column("Category",width=150,anchor=W)
set_expense_table.column("Description",width=300,anchor=W)

set_expense_table.pack(fill=BOTH,expand=True)

# Initialize and Display Expenses
display_expenses()

# Run the Application
root.mainloop()

# END
