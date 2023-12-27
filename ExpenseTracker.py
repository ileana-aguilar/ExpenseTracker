import pandas as pd
import matplotlib.pyplot as plt
#Database Connection
import mysql.connector
from mysql.connector import Error

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


#CRUD Operations
#Create (Insert Data) To insert data into your expenses table

def add_expense(connection, expense):
    cursor = connection.cursor()
    query = "INSERT INTO expenses (amount, date, category_id, description) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, expense)
        connection.commit()
        print("Expense added successfully")
    except Error as e:
        print(f"The error '{e}' occurred")



#Read(Query Data)/ fetch data/ get all expenses
def get_all_expenses(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM expenses"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"The error '{e}' occurred")


 # Update existing record
def update_expense(connection, expense_id, updated_info):
    cursor = connection.cursor()
    query = "UPDATE expenses SET amount = %s, date = %s, category_id = %s, description = %s WHERE expense_id = %s"
    try:
        cursor.execute(query, (*updated_info, expense_id))
        connection.commit()
        print("Expense updated successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Check if expense exists
def check_expense_exists(connection, expense_id):
    cursor = connection.cursor()
    query = "SELECT COUNT(1) FROM expenses WHERE expense_id = %s"
    cursor.execute(query, (expense_id,))
    (count,) = cursor.fetchone()
    return count > 0

# Delete a record
def delete_expense(connection, expense_id):
    cursor = connection.cursor()
    query = "DELETE FROM expenses WHERE expense_id = %s"
    try:
        cursor.execute(query, (expense_id,))
        connection.commit()
        print("Expense deleted successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

#Data Visualization
def get_expense_by_category(connection):
    cursor = connection.cursor()
    query = "SELECT c.name, SUM(e.amount) FROM expenses e INNER JOIN categories c ON e.category_id = c.category_id GROUP BY c.name"
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=['Category', 'Total'])

def plot_expenses(df):
    plt.figure(figsize=(10, 5))
    plt.bar(df['Category'], df['Total'], color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Total Expenses')
    plt.title('Expenses by Category')
    plt.show()



def main():
    # Database connection/ visual setup
    host = "localhost"
    database = "ExpenseTracker"
    user = "root"
    password = ""
    connection = create_db_connection(host, user, password, database)
    df = get_expense_by_category(connection)
    plot_expenses(df)

    # Operations
    expense_id_to_delete = 22
    if check_expense_exists(connection, expense_id_to_delete):
        delete_expense(connection, expense_id_to_delete)
    else:
        print(f"No expense found with ID {expense_id_to_delete}")

    '''
    expense_data = (50.0, '2023-01-01', 3, 'Grocery shopping')
    add_expense(connection, expense_data)


    expense_data = (15.50, '2023-01-01', 2, 'Lunch at cafe')
    add_expense(connection, expense_data)
    '''
    
    update_info = (75.0, '2023-01-02', 3, 'Dinner with friends')
    expense_id_to_update = 10
    update_expense(connection, expense_id_to_update, update_info)


    print('Expenses')
    expenses = get_all_expenses(connection)
    for expense in expenses:
        print(expense)

    # Close the database connection
    connection.close()

if __name__ == "__main__":
    main()
