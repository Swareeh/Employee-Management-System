#Connecting to MYSQL
import mysql.connector as ms

from tabulate import tabulate

con = ms.connect(user='root',host='localhost',passwd='1234')
cur = con.cursor()

# Fetch Current Time
def TimeStamp():
    import datetime;
    currentTime = datetime.datetime.now()
    return currentTime

#Generate a new employee ID
def GenEmployeeID():
    cur.execute('SELECT EmployeeID from employees')
    data = cur.fetchall()
    if data == []:
        return '001'
    lastID = data[0][-1]
    newID = str(int(lastID)+1)
    #Making sure the ID is min 3 Digits (Code will fail if ID exceeds 4 digts)
    while len(newID)<3:
        newID = '0' +newID
    return newID

#TODO: def Authenticate(): [Shift some info from employee table to a new Auth Table]

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
    cur.execute("INSERT into credentials values('{}','{}','{}','{}','{}')".format(EmployeeID,Name,Admin_Access,EmailID,Password))
    cur.execute("INSERT into employees values('{}','{}','{}',{},'{}','{}','{}','{}',{},'{}','{}')".format(EmployeeID,Name,Designation,Salary,EmailID,PhoneNo,DOB,MartialStatus,Children,Qualification,'Employed'))
    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(EmployeeID,Name,'New Employee Registered',AuthBY,TimeStamp()))
    con.commit()
    print('Your Employee ID:',EmployeeID)

def RemoveEmployee(AuthBY):
    Rm_EmployeeID = input('Enter EmployeeID(Removal): ')
    cur.execute("SELECT * from employees where EmployeeID='{}'".format(Rm_EmployeeID))
    data = cur.fetchone()
    Rm_Name = data[1]

    cur.execute("DELETE from employees where EmployeeID='{}'".format(Rm_EmployeeID))
    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(Rm_EmployeeID,Rm_Name,'Employee Terminated',AuthBY,TimeStamp()))
    con.commit()
    #TODO: ask for confirmation
    print(Rm_Name,'has been Terminated!')

# TODO: def SearchEmployee(AuthBY):


#First Run Esstentials
def setup():
    #TODO: company_name = input('Enter Company Name: ')
    cur.execute('CREATE database if not exists emp')
    cur.execute('USE EMP')
    #Creating a table to store employee Information
    cur.execute('CREATE table if not exists employees(EmployeeID varchar(10),Name varchar(30),Job_Title varchar(30),Salary int,EmailID varchar(50),Phone_Number varchar(17),Date_OF_Birth date,Marital_Status varchar(10),Children int,Qualification varchar(20))')
    # Authentication Table
    cur.execute('CREATE table if not exists Credentials(EmployeeID varchar(10),Name varchar(30),Admin_Access varchar(5),EmailID varchar(50),Password varchar(30))')
    #Creating table to log all events 
    cur.execute('CREATE table if not exists logs(EmployeeID varchar(10),Name varchar(30),Action varchar(50),Authorized_BY varchar(100),TimeStamp varchar(30))')
    #Creating a table to store requests from employees
    cur.execute('CREATE table if not exists requests(EmployeeID varchar(10),Name varchar(30),Requests varchar(300),Status varchar(30),TimeStamp varchar(30))')

    cur.execute('SELECT Admin_Access FROM Credentials')
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

        cur.execute("SELECT EmployeeID,Name,Admin_Access from credentials where EmailID='{}' and password='{}'".format(EmailID,Password))
        data = cur.fetchone()
        for i in data:
            LoggedInEmployeeID = data[0]
            LoggedInName = data[1]
            LoggedInAdmin_Access = data[2]


        #Admin's Tools
        if LoggedInAdmin_Access == 'True':
            print('\nWelcome',LoggedInName+'!')
            cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(LoggedInEmployeeID,LoggedInName,'[Admin] Logged in','SYSTEM',TimeStamp()))
            con.commit()

            while True:
                menu_admin = input('\n1.Add Employee\n2.Remove Employee\n3.Search Employee Detials\n4.Update Employee Details\n5.Requests & Complains\n6.Log Out\nOption: ')
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

                elif menu_admin == '2':
                    RemoveEmployee(LoggedInName)

                #Allowing admin to search for employees
                elif menu_admin == '3':
                    Srch_EmailID = input('Enter Employee EmailID: ')
                    cur.execute("SELECT * FROM Employees where EmailID='{}'".format(Srch_EmailID))
                    data = cur.fetchall()

                    if data == []:
                        print('No Data Found!')
                        break
                    print(data)

                    columns = ['EmployeeID','Name','Job Title','Salary','Email ID','Phone Number','Date of Birth','Marital Status','Children','Qualification','Employment Status']
                    print(tabulate(data,headers=columns, tablefmt='grid'))

                    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(data[0][0],data[0][1],'Employee Searched',LoggedInName,TimeStamp()))
                    con.commit()

                #TODO: Update Employees Details [add password reset feature]
                elif menu_admin == '4':
                    print('Under Dev')
                    # Updt_EmployeeID = input('Enter Employee ID: ')
                    # cur.execute("SELECT name from credentials where EmployeeID='{}'".format(Updt_EmployeeID))
                    # data = cur.fetchone()
                    # Updt_EmployeeName = data[0]
                    # updt_menu = input('What would you like to update?:\n1.Name\n2.Job_Title\n3.Admin_Access\n4.Salary\n5.EmailID\n6.Phone_Number\n7.Date_of_Birth\n8.Maritial_Status\n9.Children\n10.Qualification')

                    # if updt_menu == 'Admin_Access':

                    #     updt_menu2 = input('Input New Data(True\False): ')
                    #     cur.execute("UPDATE credentials set Admin_Access='{}' where EmployeeID='{}'".format(updt_menu2,Updt_EmployeeID))
                    #     cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(Updt_EmployeeID,Updt_EmployeeName,'Employee details Updated',LoggedInName,TimeStamp()))
                    #     con.commit()

                    # elif updt_menu == 'Salary':
                    #     updt_salary = int(input('Enter new salary amt: '))

                    # elif updt_menu == 'Children':
                    #     updt_childern = int(input('Enter new children count: '))

                    # elif updt_menu == 'Date_of_Birth':
                    #     updt_date = input('Enter new DOB(yyyy-mm-dd): ')
                    
                    # else:
                    #     updt_value = input('Enter new value: ')

                elif menu_admin == '5':
                    print('Under dev')

                elif menu_admin == '6':
                    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(LoggedInEmployeeID,LoggedInName,'[Admin] Logged Out','SYSTEM',TimeStamp()))
                    con.commit()
                    break

        #Employee's Tools
        else:
            print('\nWelcome',LoggedInName+'!')
            cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(LoggedInEmployeeID,LoggedInName,'Logged in','SYSTEM',TimeStamp()))
            con.commit()

            while True:
                menu1 = input('\n1.Requests & Complains\n2.Reset Password\n3.Log Out\nOption: ')
                if menu1 == '1':
                    print('Under dev')

                elif menu1 == '2':
                    #TODO: Add Password Confirmation
                    newPassword = input('Enter new Password: ')
                    cur.execute("UPDATE credentials set password='{}' where EmployeeID ='{}'".format(newPassword,LoggedInEmployeeID))
                    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(LoggedInEmployeeID,LoggedInName,'Password Changed',LoggedInName,TimeStamp()))
                    con.commit()
                    print('Password Updated!')

                elif menu1 == '3':
                    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(LoggedInEmployeeID,LoggedInName,'Logged Out','SYSTEM',TimeStamp()))
                    con.commit()
                    break


    elif menu == '2':
        con.close()
        break