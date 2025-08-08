#Connecting to MYSQL
import mysql.connector as ms

con = ms.connect(user='root',host='localhost',passwd='1234')
cur = con.cursor()

# Fetch Current Time
def TimeStamp():
    import datetime;
    currentTime = datetime.datetime.now()
    return currentTime

# TODO: Generate a new employee ID [THIS IS NOW INDEPENDENT]
def GenEmployeeID():
    return '001'

#TODO: def Authentication():


# Adding Employees to the Employee Table
def AddEmployee(AuthBY,Admin_Access='False'):
        EmployeeID = GenEmployeeID()
        Name = input('Enter name of Employee: ')
        DOB = input('Enter Date of Birth of Employee(yyyy-mm-dd): ')
        EmailID = input('Enter Email ID of Employee: ').lower()
        PhoneNo = input('Enter Phone Number of Employee: ')
        Designation = input('Enter Employee Job Title: ')
        MartialStatus = input('Enter Marital Status of Employee: ')
        Children = int(input('Enter no. of children of Employee: '))
        Salary = int(input('Enter Salary of Employee: '))
        Qualification = input('Enter Qualification of Employee: ')
        Password = input('Create a password: ')

        cur.execute("INSERT into employees values('{}','{}','{}','{}',{},'{}','{}','{}','{}',{},'{}','{}','{}')".format(EmployeeID,Name,Designation,Admin_Access,Salary,EmailID,PhoneNo,DOB,MartialStatus,Children,Qualification,'Employed',Password))
        cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(EmployeeID,Name,'New Employee Registered',AuthBY,TimeStamp()))
        con.commit()
        print('Your Employee ID:',EmployeeID)

#First Run Esstentials
def setup():
    #TODO: company_name = input('Enter Company Name: ')
    cur.execute('CREATE database if not exists emp')
    cur.execute('USE EMP')
    #Creating a table to store employee Information
    cur.execute('CREATE table if not exists employees(EmployeeID varchar(10),Name varchar(30),Job_Title varchar(30),Admin_Access varchar(5),Salary int,EmailID varchar(50),Phone_Number varchar(17),Date_OF_Birth date,Marital_Status varchar(10),Children int,Qualifications varchar(20),Employment_Status varchar(15),Password varchar(30))')
    #Creating table to log all events 
    cur.execute('CREATE table if not exists logs(EmployeeID varchar(10),Name varchar(30),Action varchar(50),Authorized_BY varchar(100),TimeStamp varchar(30))')
    #Creating a table to store requests from employees
    cur.execute('CREATE table if not exists requests(EmployeeID varchar(10),Name varchar(30),Requests varchar(300),Status varchar(30),TimeStamp varchar(30))')

    cur.execute('SELECT Admin_Access FROM EMPLOYEES')
    data = cur.fetchall()

    #Checking if an Admin Exists
    AdminExists = False
    for i in data:
        for j in i:
            if j == 'True':
                AdminExists = True
                break
    if AdminExists == False:
        #Creating an account for Admin if it does not exist
        print('ADMIN ACCOUNT CREATION:')
        AddEmployee('SYSTEM','True')
        print('Admin Registered!')

setup()

print('\nWELCOME TO Employee Management System!')

while True:
    menu = input('\n1.Login\n2.Exit\nOption: ')

    if menu == '1':


        EmailID = input('Enter Email ID: ').lower()
        Password = input('Enter Password: ')

        cur.execute("SELECT EmployeeID,Name,Job_Title,Admin_Access from employees where EmailID='{}' and password='{}'".format(EmailID,Password))
        data = cur.fetchone()
        for i in data:
            EmployeeID = data[0]
            LoggedInName = data[1]
            title = data[2]
            Admin_Access = data[3]


        #Admin's Tools
        if Admin_Access == 'True':
            print('\nWelcome',LoggedInName+'!')
            cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(EmployeeID,LoggedInName,'[Admin] Logged in','SYSTEM',TimeStamp()))
            con.commit()

            while True:
                menu_admin = input('\n1.Add Employee\n2.Remove Employee\n3.Update Employee Details\n4.Employee Requests\n5.Employee Complaints\n6.Log Out\nOption: ')
                #Allowing admin to add employees
                if menu_admin == '1':
                    while True:
                        menu_admin2 = input('Give new employee admin access?(YES/NO): ')
                        #TODO: Ask for confirmation
                        if menu_admin2  == 'YES':
                            AddEmployee(LoggedInName,'True')
                            print('New Admin Registered!')
                            break
                        elif menu_admin2 == 'NO':
                            AddEmployee(LoggedInName,'False')
                            print('New Employee Registered!')
                            break

                #Allowing admin to remove employees
                elif menu_admin == '2':
                    Rm_EmployeeID = input('Enter EmployeeID(Removal): ')
                    cur.execute("SELECT * from employees where EmployeeID='{}'".format(Rm_EmployeeID))
                    data = cur.fetchone()
                    Rm_Name = data[1]

                    cur.execute("DELETE from employees where EmployeeID='{}'".format(Rm_EmployeeID))
                    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(Rm_EmployeeID,Rm_Name,'Employee Terminated',LoggedInName,TimeStamp()))
                    con.commit()
                    #TODO: ask for confirmation
                    print(Rm_Name,'has been Terminated!')

                #TODO: Allowing admin to update employee details
                elif menu_admin == '3':
                    print('INDEV')
                    

                elif menu_admin == '6':
                    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(EmployeeID,LoggedInName,'[Admin] Logged Out','SYSTEM',TimeStamp()))
                    con.commit()
                    break


        #Employee's Tools
        else:
            print('\nWelcome',LoggedInName+'!')
            cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(EmployeeID,LoggedInName,'Logged in','SYSTEM',TimeStamp()))
            con.commit()

            while True:
                menu1 = input('\n1.Requests\n2.Log Out\nOption: ')
                if menu1 == '2':
                    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(EmployeeID,LoggedInName,'Logged Out','SYSTEM',TimeStamp()))
                    con.commit()
                    break


    elif menu == '2':
        con.close()
        break