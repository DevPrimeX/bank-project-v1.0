# The code officially design and written by Naresh Choyal 
# Dont remove credit

import mysql.connector
import time

# Establish MySQL connection
cnx = mysql.connector.connect(user='your_username', password='your_password',
                              host='localhost', database='hospital_db')
cursor = cnx.cursor()

# Create necessary tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_name VARCHAR(255),
    specialization VARCHAR(255)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255),
    age INT,
    gender VARCHAR(50)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT,
    patient_id INT,
    appointment_date DATE,
    appointment_time TIME,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
)
''')

# Check if doctors exist, if not add default doctors
query = '''SELECT * FROM Doctors'''
cursor.execute(query)
results = cursor.fetchall()
if results == []:
    cursor.execute('''
                    INSERT INTO Doctors (doctor_name, specialization)
                    VALUES
                    ('Dr. John Doe', 'Cardiology'),
                    ('Dr. Jane Smith', 'Neurology'),
                    ('Dr. Emily Davis', 'Orthopedics')
                    ''')
    cnx.commit()

def main():
    inloop = True
    while inloop:
        print("\n---------------------------------------------------------------------")
        print("---------------------Welcome to the Hospital Management System!---------------------")
        print("---------------------------------------------------------------------")
        print("How do you want to enter?")
        print("Choice 1: Admin Login\nChoice 2: Patient Login\nChoice 3: Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            admin_login(cnx, cursor)
        elif choice == '2':
            patient_login(cnx, cursor)
        elif choice == '3':
            exit()
        else:
            print("Invalid Choice!")

def admin_login(cnx, cursor):
    # Ask for Admin Username and Password
    print("\n---------Welcome! Please login as Admin!----------")
    
    username = input("Enter admin username: ")
    
    # Check the username and password
    if username == 'prime':
        password = input("Enter the password: ")  # No more hiding the password
        
        if password == "admin123":
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
        print("Choice 1: Add a Doctor\nChoice 2: Remove a Doctor\nChoice 3: View Doctors")
        print("Choice 4: View All Appointments\nChoice 5: Exit")
        
        choice = int(input("Enter your choice: "))
        print()
        time.sleep(0.5)

        if choice == 1:
            print("What would you like to add?")
            doctor_name = input("Enter doctor name: ")
            specialization = input("Enter specialization: ")

            try:
                query = f"INSERT INTO Doctors (doctor_name, specialization) VALUES ('{doctor_name}', '{specialization}')"
                cursor.execute(query)
                cnx.commit()
                print("The doctor has been added to the system!")
            except Exception as e:
                print("Error occurred!")
            
            time.sleep(1)

        elif choice == 2:
            display_doctors(cursor)
            print("Which doctor would you like to remove?")
            id = int(input("Enter doctor id: "))
            try:
                query = f"DELETE FROM Doctors WHERE doctor_id={id}"
                cursor.execute(query)
                cnx.commit()
                print("The doctor has been removed from the system!")
            except Exception as e:
                print("Invalid doctor!")
            time.sleep(1)

        elif choice == 3:
            display_doctors(cursor)
            time.sleep(1.5)

        elif choice == 4:
            display_appointments(cursor)
            time.sleep(1.5)

        elif choice == 5:
            inloop = False
            main()

        else:
            print("Invalid Choice!")
            time.sleep(1)

def display_doctors(cursor):
    query = '''SELECT * FROM Doctors'''
    cursor.execute(query)
    results = cursor.fetchall()
    print("List of Doctors: ")
    print("ID", "Name", "Specialization", sep=" ")
    for each in results:
        print(each[0], each[1], each[2], sep=" ")

def display_appointments(cursor):
    query = '''SELECT a.appointment_id, d.doctor_name, p.patient_name, a.appointment_date, a.appointment_time
               FROM Appointments a
               JOIN Doctors d ON a.doctor_id = d.doctor_id
               JOIN Patients p ON a.patient_id = p.patient_id'''
    cursor.execute(query)
    results = cursor.fetchall()
    print("Appointments: ")
    print("ID", "Doctor", "Patient", "Date", "Time", sep=" | ")
    for each in results:
        print(each[0], each[1], each[2], each[3], each[4], sep=" | ")

def patient_login(cnx, cursor):
    inloop = True
    while inloop:
        print("-----------Welcome, You are logged in as a Patient!-------------")
        print("Here is the list of choices:")
        print("Choice 1: View Doctors\nChoice 2: Book Appointment\nChoice 3: View Appointments\nChoice 4: Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            display_doctors(cursor)
            time.sleep(1)

        elif choice == 2:
            patient_name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            gender = input("Enter your gender: ")

            # Register the patient
            cursor.execute(f"INSERT INTO Patients (patient_name, age, gender) VALUES ('{patient_name}', {age}, '{gender}')")
            cnx.commit()

            patient_id = cursor.lastrowid
            print("You have been registered successfully!")

            # Book appointment
            display_doctors(cursor)
            doctor_id = int(input("Enter doctor id to book appointment: "))
            appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
            appointment_time = input("Enter appointment time (HH:MM:SS): ")

            cursor.execute(f"INSERT INTO Appointments (doctor_id, patient_id, appointment_date, appointment_time) VALUES ({doctor_id}, {patient_id}, '{appointment_date}', '{appointment_time}')")
            cnx.commit()
            print("Your appointment has been booked!")

            time.sleep(1)

        elif choice == 3:
            patient_name = input("Enter your name: ")
            query = f"SELECT * FROM Patients WHERE patient_name = '{patient_name}'"
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                patient_id = result[0]
                print(f"Your appointments: ")
                query = f"SELECT a.appointment_date, a.appointment_time, d.doctor_name FROM Appointments a JOIN Doctors d ON a.doctor_id = d.doctor_id WHERE a.patient_id = {patient_id}"
                cursor.execute(query)
                appointments = cursor.fetchall()
                for appointment in appointments:
                    print(f"Date: {appointment[0]} | Time: {appointment[1]} | Doctor: {appointment[2]}")
            else:
                print("Patient not found!")

            time.sleep(1)

        elif choice == 4:
            inloop = False
            main()

        else:
            print("Invalid Choice!")
            time.sleep(1)

# Start the application
main()

# Close the connection at the end
cnx.close()
