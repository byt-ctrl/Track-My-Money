/* The expenses table controls individual expense records through its data storage structure. 
The expense records contain four mandatory fields named ID, date, amount and category and description.
The system maintains valid and positive amount validation. */



CREATE TABLE IF NOT EXISTS expenses 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT NOT NULL,amount REAL NOT NULL CHECK (amount>0),category TEXT NOT NULL,
    description TEXT
);



/* The expense categories table contains unique recorded Expense categories.
The categories table consists of two columns for both IDs and names. */

CREATE TABLE IF NOT EXISTS categories 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL UNIQUE
);


/* A budgets table creates monthly budget records which must stay at or above zero value.
A budget needs to be associated with a particular month and must hold only positive numbers. */

CREATE TABLE IF NOT EXISTS budgets 
(
    month TEXT PRIMARY KEY,budget REAL NOT NULL CHECK (budget>=0)
)
;

/* The category_budget table allows users to set specific budgets
for individual expense categories. */


CREATE TABLE IF NOT EXISTS category_budget 
(
    category TEXT PRIMARY KEY,budget REAL NOT NULL CHECK (budget >= 0)
)
;
