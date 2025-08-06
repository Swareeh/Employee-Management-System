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

    HR_name = input('Enter name of HR: ')
    HR_dob = input('Enter Date of Birth of HR(yyyy-mm-dd): ')
    HR_emailID = input('Enter Email ID of HR: ')
    HR_phoneNo = input('Enter Phone Number of HR: ')
    HR_martialStatus = input('Enter Marital Status of HR: ')
    HR_Children = int(input('Enter no. of children of HR: '))
    HR_Salary = int(input('Enter Salary of HR: '))
    HR_Qualification = input('Enter Qualification of HR: ')
    HR_password = input('Create a password: ')

    cur.execute("INSERT into employees values('{}','{}','{}',{},'{}','{}','{}','{}',{},'{}','{}','{}')".format(GenEmployeeID(),HR_name,'Human Resource',HR_Salary,HR_emailID,HR_phoneNo,HR_dob,HR_martialStatus,HR_Children,HR_Qualification,'Employed',HR_password))
    con.commit()
    print('HR Registered!')

setup()