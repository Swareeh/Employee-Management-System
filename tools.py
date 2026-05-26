#Importing required packages
import mysql.connector as ms

#Presents data in table format
from tabulate import tabulate

#Connecting to MYSQL
con = ms.connect(user='root',host='localhost',passwd='1234')
cur = con.cursor()


#SYSTEM TOOLS -------------------------------------------------------------------

# First Run---------
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
    cur.execute('CREATE table if not exists requests(EmployeeID varchar(10),Name varchar(30),Request varchar(300),Status varchar(30),Authorized_BY varchar(100),TimeStamp varchar(30))')

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
    lastID = data[-1][-1]
    newID = str(int(lastID)+1)
    #Making sure the ID is min 3 Digits (Code will fail if ID exceeds 4 digts)
    while len(newID)<3:
        newID = '0' +newID
    return newID

#Authenticating the user via login credentials
def Authenticate():
    EmailID = input('Enter Email ID: ').lower()
    Password = input('Enter Password: ')

    cur.execute("SELECT EmployeeID,Name,Admin_Access from credentials where EmailID='{}' and password='{}'".format(EmailID,Password))
    data = cur.fetchone()
    if data == None:
        print('Invalid Credentials!')
        return
    return data[0],data[1],data[2] # EmployeeID,EmployeeName,AdminAccess


#ADMIN TOOLS --------------------------------------------------------------------

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
    cur.execute("DELETE from credentials where EmployeeID='{}'".format(Rm_EmployeeID))
    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(Rm_EmployeeID,Rm_Name,'Employee Terminated',AuthBY,TimeStamp()))
    con.commit()
    #TODO: ask for confirmation
    print(Rm_Name,'has been Terminated!')



# You need to convert all the features into functions.

def SearchEmployee(AuthBY):
    Srch_EmailID = input('Enter Employee EmailID: ')
    cur.execute("SELECT * FROM Employees where EmailID='{}'".format(Srch_EmailID))
    data = cur.fetchall()

    if data == []:
        print('No Data Found!')
        return
    print(data)

    columns = ['EmployeeID','Name','Job Title','Salary','Email ID','Phone Number','Date of Birth','Marital Status','Children','Qualification','Employment Status']
    print(tabulate(data,headers=columns, tablefmt='grid'))

    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(data[0][0],data[0][1],'Employee Searched',AuthBY,TimeStamp()))
    con.commit()