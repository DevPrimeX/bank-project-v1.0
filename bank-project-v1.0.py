
import datetime as date
import mysql.connector as sql

SpecialSym = ['$', '@', '#', '%']
dates1 = date.datetime.now()

mycon = sql.connect(host="localhost", user="root", password="tiger123", database="trial")
mycur = mycon.cursor()

def create_tables():
    bank_table_query = """
    CREATE TABLE IF NOT EXISTS bank (
        Name VARCHAR(100),
        UserName VARCHAR(50) PRIMARY KEY,
        Password VARCHAR(50),
        DOB DATE,
        Address TEXT,
        Mobile_Number VARCHAR(10),
        Aadhar_no VARCHAR(12),
        Balance DECIMAL(10, 2)
    );
    """

    transaction_table_query = """
    CREATE TABLE IF NOT EXISTS transaction (
        Credited DECIMAL(10, 2),
        Debited DECIMAL(10, 2),
        UserName1 VARCHAR(50),
        Date DATETIME,
        FOREIGN KEY (UserName1) REFERENCES bank(UserName)
    );
    """

    mycur.execute(bank_table_query)
    mycur.execute(transaction_table_query)
    mycon.commit()

def main_menu():
    while True:
        print("\n")
        print("___________________________________________________________________________")
        print("*******************  Welcome To Central Bank Of India  *******************")
        print("____________________________________________________________________________")
        print("Press 1 to for Sign Up ")
        print("Press 2 to for Sign In  ")

        try:
            choice = int(input("Enter Your Choice: "))
            if choice not in [1, 2]:
                raise ValueError("Invalid choice. Please enter 1 or 2.")
            return choice
        except ValueError as ve:
            print(ve)

def validate_name(name):
    special_characters = ['.', '#', '$', '*', '&', '=', ',', '@', '?', '/']
    if any(char in name for char in special_characters):
        raise ValueError("Special characters are not allowed in the name.")

def validate_username(username):
    special_characters = ['.', '#', '$', '*', '&', '=', ',', '@', '?', '/']
    if any(char in username for char in special_characters):
        raise ValueError("Special characters are not allowed in the username.")

def validate_password(password):
    if len(password) < 6:
        raise ValueError("Password should contain at least 6 characters.")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password should contain at least one number.")
    if not any(char.isupper() for char in password):
        raise ValueError("Password should contain at least one uppercase letter.")
    if not any(char.islower() for char in password):
        raise ValueError("Password should contain at least one lowercase letter.")
    if not any(char in SpecialSym for char in password):
        raise ValueError("Password should contain at least one special character.")

def sign_up():
    while True:
        try:
            name = input("Enter Your Name Here: ")
            validate_name(name)
            break
        except ValueError as ve:
            print(ve)

    while True:
        try:
            username = input("Enter Your Username: ")
            validate_username(username)
            break
        except ValueError as ve:
            print(ve)

    while True:
        try:
            password = input("Enter Your Password: ")
            validate_password(password)
            break
        except ValueError as ve:
            print(ve)

    while True:
        try:
            deposit = int(input("Enter the Amount of Money You Want to Deposit: "))
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            dob = input("Enter Your Date of Birth (DD/MM/YYYY): ")
            dob = date.datetime.strptime(dob, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Please enter Date of Birth in proper format (DD/MM/YYYY).")

    address = input("Enter Your Address: ")

    while True:
        try:
            phone = input("Enter Your Phone Number: ")
            if len(phone) != 10 or not phone.isdigit():
                raise ValueError("Please enter a valid 10 digit number.")
            break
        except ValueError as ve:
            print(ve)

    while True:
        try:
            aadhar = input("Enter Your 12 Digit Aadhar Number: ")
            if len(aadhar) != 12 or not aadhar.isdigit():
                raise ValueError("Please enter a valid 12 digit Aadhar number.")
            break
        except ValueError as ve:
            print(ve)

    query = f"INSERT INTO bank VALUES('{name}', '{username}', '{password}', '{dob}', '{address}', '{phone}', '{aadhar}', '{deposit}')"
    mycur.execute(query)
    mycon.commit()
    print("\n")
    print("_________________________________________________________________________")
    print("*********** Account Has Been Created Successfully, Kindly Login ************")
    print("_________________________________________________________________________")

def sign_in():
    while True:
        username = input("Enter Your Username: ")
        password = input("Enter Your Password: ")

        query = f"SELECT * FROM bank WHERE UserName='{username}' AND Password='{password}'"
        mycur.execute(query)
        data = mycur.fetchall()

        if data:
            return username
        else:
            print("Login Failed. Please Try Again.")

def user_menu(username):
    while True:
        print("\n")
        print("___________________________________________________________________________")
        print("*************** Welcome To Central Bank Of India : *************************")
        print("___________________________________________________________________________")
        print("\n")
        print("Press 1 To Withdraw Money")
        print("Press 2 To Deposit Money")
        print("Press 3 to View Last Five Transactions")
        print("Press 4 To View Your Profile")
        print("Press 5 To Update Account Details")
        print("Press 6 to Delete Your Account Permanently")
        print("Press 7 to Log Out")

        try:
            choice = int(input("Enter Your Choice: "))
            if choice not in range(1, 8):
                raise ValueError("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError as ve:
            print(ve)
            continue

        if choice == 1:
            withdraw_money(username)
        elif choice == 2:
            deposit_money(username)
        elif choice == 3:
            view_transactions(username)
        elif choice == 4:
            view_profile(username)
        elif choice == 5:
            update_account(username)
        elif choice == 6:
            delete_account(username)
            break
        elif choice == 7:
            print("_____________________________________________________________________________")
            print("************* Thanks For Choosing Central Bank Of India *****************")
            print("____________________________________________________________________________")
            break

def withdraw_money(username):
    try:
        query = f"SELECT Balance FROM bank WHERE UserName='{username}'"
        mycur.execute(query)
        balance = mycur.fetchone()[0]
    except Exception as e:
        print("Error fetching balance:", e)
        return

    print(f"Your Account Balance is: {balance}")

    while True:
        try:
            amount = int(input("Enter the amount for withdrawal: "))
            if amount > balance:
                print("Insufficient balance. Please try again.")
                continue

            query = f"UPDATE bank SET Balance = GREATEST(0, Balance - {amount}) WHERE UserName='{username}'"
            mycur.execute(query)
            mycon.commit()

            transaction_query = f"INSERT INTO transaction VALUES(0, {amount}, '{username}', '{dates1}')"
            mycur.execute(transaction_query)
            mycon.commit()

            query = f"SELECT Balance FROM bank WHERE UserName='{username}'"
            mycur.execute(query)
            new_balance = mycur.fetchone()[0]

            print(f"Your account has been debited with Rs {amount}. Available balance is Rs {new_balance}.")
            break
        except ValueError:
            print("Please enter a valid amount.")

def deposit_money(username):
    while True:
        try:
            amount = int(input("Enter the amount to deposit: "))
            query = f"UPDATE bank SET Balance = Balance + {amount} WHERE UserName='{username}'"
            mycur.execute(query)
            mycon.commit()

            transaction_query = f"INSERT INTO transaction VALUES({amount}, 0, '{username}', '{dates1}')"
            mycur.execute(transaction_query)
            mycon.commit()

            query = f"SELECT Balance FROM bank WHERE UserName='{username}'"
            mycur.execute(query)
            new_balance = mycur.fetchone()[0]

            print(f"Your account has been credited with Rs {amount}. Available balance is Rs {new_balance}.")
            break
        except ValueError:
            print("Please enter a valid amount.")

def view_transactions(username):
    query = f"SELECT Credited, Debited, Date FROM transaction WHERE UserName1='{username}' ORDER BY Date DESC LIMIT 5"
    mycur.execute(query)
    transactions = mycur.fetchall()
    
    if not transactions:
        print("No transactions found.")
        return
    
    print("\nLast five transactions:")
    print("------------------------------------------------")
    print(f"{'Credited':<10} {'Debited':<10} {'Date':<20}")
    print("------------------------------------------------")
    
    for transaction in transactions:
        credited, debited, date = transaction
        formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{credited:<10} {debited:<10} {formatted_date:<20}")
    print("------------------------------------------------")


def view_profile(username):
    query = f"SELECT Name, UserName, Password, Address, Mobile_Number, Aadhar_no, Balance FROM bank WHERE UserName='{username}'"
    mycur.execute(query)
    profile = mycur.fetchone()

    print("Profile Details:")
    print("Name:", profile[0])
    print("Username:", profile[1])
    print("Password:", profile[2])
    print("Address:", profile[3])
    print("Mobile Number:", profile[4])
    print("Aadhar Number:", profile[5])
    print("Balance:", profile[6])

def update_account(username):
    while True:
        print("Press 1 To Update Your Name")
        print("Press 2 To Update Your Username")
        print("Press 3 To Update Your Password")
        print("Press 4 To Update Your Phone Number")
        print("Press 5 To Update Address")

        try:
            choice = int(input("Enter Your Choice: "))
            if choice not in range(1, 6):
                raise ValueError("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError as ve:
            print(ve)
            continue

        if choice == 1:
            new_name = input("Enter Your New Name: ")
            query = f"UPDATE bank SET Name='{new_name}' WHERE UserName='{username}'"
            mycur.execute(query)
            mycon.commit()
            print("Name updated successfully.")
        elif choice == 2:
            new_username = input("Enter Your New Username: ")
            query = f"UPDATE bank SET UserName='{new_username}' WHERE UserName='{username}'"
            mycur.execute(query)
            mycon.commit()
            print("Username updated successfully.")
        elif choice == 3:
            new_password = input("Enter Your New Password: ")
            validate_password(new_password)
            query = f"UPDATE bank SET Password='{new_password}' WHERE UserName='{username}'"
            mycur.execute(query)
            mycon.commit()
            print("Password updated successfully.")
        elif choice == 4:
            new_phone = input("Enter Your New Phone Number: ")
            if len(new_phone) != 10 or not new_phone.isdigit():
                print("Please enter a valid 10 digit phone number.")
                continue
            query = f"UPDATE bank SET Mobile_Number='{new_phone}' WHERE UserName='{username}'"
            mycur.execute(query)
            mycon.commit()
            print("Phone number updated successfully.")
        elif choice == 5:
            new_address = input("Enter Your New Address: ")
            query = f"UPDATE bank SET Address='{new_address}' WHERE UserName='{username}'"
            mycur.execute(query)
            mycon.commit()
            print("Address updated successfully.")
        break

def delete_account(username):
    try:
        query = f"DELETE FROM transaction WHERE UserName1='{username}'"
        mycur.execute(query)
        mycon.commit()

        query = f"DELETE FROM bank WHERE UserName='{username}'"
        mycur.execute(query)
        mycon.commit()
        
        print("Account and related transactions deleted successfully.")
    except sql.Error as err:
        print(f"Error: {err}")


def main():
    choice = main_menu()
    if choice == 1:
        sign_up()
    elif choice == 2:
        username = sign_in()
        user_menu(username)

if __name__ == "__main__":
    create_tables()
    main()

mycon.close()
