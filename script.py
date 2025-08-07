#Connecting to MYSQL
import mysql.connector as ms

con = ms.connect(user='root',host='localhost',passwd='1234')
cur = con.cursor()

# Fetch Current Time
def TimeStamp():
    import datetime;
    currentTime = datetime.datetime.now()
    return currentTime

# TODO: Generate a new employee ID
def GenEmployeeID():
    return '001'


#First Run Esstentials
def setup():
    # company_name = input('Enter Company Name: ')
    cur.execute('CREATE database if not exists emp')
    cur.execute('USE EMP')
    cur.execute('CREATE table if not exists employees(EmployeeID varchar(10),Name varchar(30),Job_Title varchar(30),Salary int,EmailID varchar(50),Phone_Number varchar(17),Date_OF_Birth date,Marital_Status varchar(10),Children int,Qualifications varchar(20),Employment_Status varchar(15),Password varchar(30))')
    cur.execute('CREATE table if not exists logs(EmployeeID varchar(10),Name varchar(30),Action varchar(50),TimeStamp varchar(30))')

    cur.execute('SELECT * FROM EMPLOYEES')
    data = cur.fetchone()
    try:
        if data[0] == '001':
            return
    except:
        Adm_EID = '001'
        Adm_name = input('Enter name of Admin: ')
        Adm_dob = input('Enter Date of Birth of Admin(yyyy-mm-dd): ')
        Adm_emailID = input('Enter Email ID of Admin: ').lower()
        Adm_phoneNo = input('Enter Phone Number of Admin: ')
        Adm_Title = input('Enter Admin Job Title: ')
        Adm_martialStatus = input('Enter Marital Status of Admin: ')
        Adm_Children = int(input('Enter no. of children of Admin: '))
        Adm_Salary = int(input('Enter Salary of Admin: '))
        Adm_Qualification = input('Enter Qualification of Admin: ')
        Adm_password = input('Create a password: ')

        cur.execute("INSERT into employees values('{}','{}','{}',{},'{}','{}','{}','{}',{},'{}','{}','{}')".format(Adm_EID,Adm_name,Adm_Title,Adm_Salary,Adm_emailID,Adm_phoneNo,Adm_dob,Adm_martialStatus,Adm_Children,Adm_Qualification,'Employed',Adm_password))
        cur.execute("INSERT into logs values('{}','{}','{}','{}')".format(Adm_EID,Adm_name,'EMP Setup Complete',TimeStamp()))
        con.commit()
        print('Admin Registered!')

setup()

print('WELCOME TO EMP')

while True:
    menu = input('\n1.Login\n2.Exit\nOption: ')

    if menu == '1':


        EmailID = input('Enter Email ID: ').lower()
        Password = input('Enter Password: ')

        cur.execute("SELECT EmployeeID,Name,Job_Title from employees where EmailID='{}' and password='{}'".format(EmailID,Password))
        data = cur.fetchone()
        for i in data:
            EmployeeID = data[0]
            EmployeeName = data[1]
            title = data[2]


        #Admin Controls
        if EmployeeID == '001':
            print('\nWelcome',EmployeeName,'!')
            cur.execute("INSERT into logs values('{}','{}','{}','{}')".format(EmployeeID,EmployeeName,'[Admin] Logged in',TimeStamp()))
            con.commit()

            while True:
                menu1 = input('\n1.Requests\n2.Log Out\nOption: ')
                if menu1 == '2':
                    break



        #Employee Controls
        elif EmployeeID != '001':
            print('\nWelcome',EmployeeName,'!')
            cur.execute("INSERT into logs values('{}','{}','{}','{}')".format(EmployeeID,EmployeeName,'Logged in',TimeStamp()))
            con.commit()

            while True:
                menu1 = input('\n1.Requests\n2.Log Out\nOption: ')
                if menu1 == '2':
                    break






    elif menu == '2':
        break