# The code officially design and written by Naresh Choyal 
# Dont remove credit

import mysql.connector
import time

# Establish MySQL connection
cnx = mysql.connector.connect(user='your_username', password='your_password',
                              host='localhost', database='menu_db')
cursor = cnx.cursor()

# Create Menu table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Menu (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    product_price INT
)
''')

# Check if the table is empty, and if so, insert default menu items
query = '''SELECT * FROM Menu'''
cursor.execute(query)
results = cursor.fetchall()
if results == []:
    cursor.execute('''
                    INSERT INTO Menu (product_name, product_price)
                    VALUES
                    ('Cake', 400),
                    ('Bread', 50),
                    ('Cookies', 100),
                    ('Doughnuts', 80),
                    ('Pie', 120)
                    ''')
    cnx.commit()

def main():
    inloop = True
    while inloop:
        print("\n---------------------------------------------------------------------")
        print("---------------------Welcome to Slice of Heaven Bakery!---------------------")
        print("---------------------------------------------------------------------")
        print("How do you want to enter?")
        print("Choice 1: Admin Login\nChoice 2: Customer Login\nChoice 3: Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            admin_login(cnx, cursor)
        elif choice == '2':
            customer_login(cnx, cursor)
        elif choice == '3':
            exit()
        else:
            print("Invalid Choice!")

def admin_login(cnx, cursor):
    # Ask for Admin Username and Password
    print("\n---------Welcome! Please login as Admin!----------")
    
    username = input("Enter admin username: ")
    
    # Check the username and password
    if username == 'norace': #Dont remove the username name 
        password = input("Enter the password: ") 
        
        if password == "Norace":
            print("Password verified.")
            admin_panel(cnx, cursor)
        else:
            print("Incorrect password!")
            time.sleep(1)
    else:
        print("Incorrect username!")
        time.sleep(1)

def admin_panel(cnx, cursor):
    inloop = True
    while inloop:
        print("\n---------Welcome! You are logged in as Admin!----------")
        print("Here are the list of choices:")
        print("Choice 1: Add an item\nChoice 2: Remove an item\nChoice 3: Update item price")
        print("Choice 4: See all the items\nChoice 5: Exit")
        
        choice = int(input("Enter your choice: "))
        print()
        time.sleep(0.5)

        if choice == 1:
            print("What would you like to add?")
            product_name = input("Enter product name: ")
            product_price = input("Enter product price: ")

            try:
                query = f"INSERT INTO Menu (product_name, product_price) VALUES ('{product_name}', '{product_price}')"
                cursor.execute(query)
                cnx.commit()
                print("The item has been added to the list!")
            except Exception as e:
                print("Error occurred!")
            
            time.sleep(1)

        elif choice == 2:
            display_items(cursor)
            print("Which item would you like to remove?")
            id = int(input("Enter product id: "))
            try:
                query = f"DELETE FROM Menu WHERE product_id={id}"
                cursor.execute(query)
                cnx.commit()
                print("The item has been removed from the shop!")
            except Exception as e:
                print("Invalid item!")
            time.sleep(1)

        elif choice == 3:
            display_items(cursor)
            print("Which item's price would you like to update?")
            id = int(input("Enter product ID: "))
            price = int(input("Enter the updated price: "))
            try:
                query = f"UPDATE Menu SET product_price={price} WHERE product_id={id}"
                cursor.execute(query)
                cnx.commit()
                print("The item price has been updated!")
            except Exception as e:
                print("Invalid Product ID!")
            time.sleep(1)

        elif choice == 4:
            display_items(cursor)
            time.sleep(1.5)

        elif choice == 5:
            inloop = False
            main()

        else:
            print("Invalid Choice!")
            time.sleep(1)

def display_items(cursor):
    query = '''SELECT * FROM Menu'''
    cursor.execute(query)
    results = cursor.fetchall()
    print("List of items: ")
    print("ID", "Name", "Price", sep=" ")
    for each in results:
        print(each[0], each[1], each[2], sep=" ")

def customer_login(cnx, cursor):
    inloop = True
    while inloop:
        print("-----------Welcome, You are logged in as a biller!-------------")
        print("Here is the list of choices:")
        print("Choice 1: Billing\nChoice 2: Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            name = input("Enter the customer name: ")
            print(f"What do you want to buy, {name}?")
            time.sleep(0.5)
            display_items(cursor)

            print()
            total = 0
            items = []
            while True:
                id = int(input("Enter the product ID: "))
                quantity = int(input("Enter the quantity: "))
                try:
                    query = f"SELECT * FROM Menu WHERE product_id={id}"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    
                    total += result[2] * quantity
                    items.append([result[1], quantity])
                    i = input("Anything else? Answer Y for Yes and N for No! ")
                    if i == 'N':
                        break
                except Exception as e:
                    print("Invalid Entry!")
                    print(e)
                    break
            
            if total != 0:
                print("\n---------Slice of Heaven Bakery!--------")
                print("-------Billing Details-------")
                print(f"Name: {name}")
                print("Items:")
                for each in items:
                    print(f"{each[0]}: {each[1]}")
                print(f"Total: {total}")
                print("Thank you! Have a sweet day!")
                print()

            time.sleep(1)

        elif choice == 2:
            inloop = False
            main()

        else:
            print("Invalid Choice!")
            time.sleep(1)

# Start the application
main()

# Close the connection at the end
cnx.close()
