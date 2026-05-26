#Importing tools
from tools import con,cur,tabulate,setup,Authenticate,TimeStamp,AddEmployee,RemoveEmployee,SearchEmployee

#Sets up missing databases and tables.
setup()

print('\nWELCOME TO Employee Management System!')

while True:
    menu = input('\n1.Login\n2.Exit\nOption: ')

    if menu == '1':

        LoggedInEmployeeID,LoggedInName,LoggedInAdmin_Access = Authenticate()

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
                    SearchEmployee(LoggedInName)

                #TODO: Update Employees Details [add password reset feature]
                
                elif menu_admin == '4':
                    Updt_EmployeeID = input('Enter Employee ID: ')
                    cur.execute("SELECT name from credentials where EmployeeID='{}'".format(Updt_EmployeeID))
                    data = cur.fetchone()
                    Updt_EmployeeName = data[0]
                    updt_menu = input('\nWhat would you like to update?:\nName\nJob_Title\nAdmin_Access\nSalary\nEmailID\nPhone_Number\nDate_of_Birth\nMaritial_Status\nChildren\nQualification\nType Option: ')

                    if updt_menu == 'Admin_Access':
                        updt_adminAccess = input('Input New Data(True/False): ')
                        cur.execute("UPDATE credentials set Admin_Access='{}' where EmployeeID='{}'".format(updt_adminAccess,Updt_EmployeeID))
                        cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(Updt_EmployeeID,Updt_EmployeeName,'Employee Admin Access Updated',LoggedInName,TimeStamp()))
                        con.commit()
                        print('Admin Access Updated')
                    
                    elif updt_menu == 'Salary':
                        updt_salary = int(input('Enter new salary amt: '))
                        cur.execute("UPDATE employees set Salary='{}' where EmployeeID='{}'".format(updt_salary,Updt_EmployeeID))


                    elif updt_menu == 'Children':
                        updt_childern = int(input('Enter new children count: '))

                    elif updt_menu == 'Date_of_Birth':
                        updt_date = input('Enter new DOB(yyyy-mm-dd): ')
                    
                    else:
                        updt_value = input('Enter new value: ')
                        cur.execute("UPDATE employees set {}='{}' where EmployeeID='{}'".format(updt_menu,updt_value,Updt_EmployeeID))
                        print('Employee',updt_menu,'Updated')

                elif menu_admin == '5':
                    cur.execute('SELECT * from requests')
                    data = cur.fetchall()
                    columns = ['EmployeeID','Name','Request','Status','Authorized BY','Time']
                    print(tabulate(data,headers=columns, tablefmt='grid'))
                    # TODO: ADD Approval\Reject features
                    
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
                    request = input('Enter your request: ') 
                    cur.execute("INSERT into requests values('{}','{}','{}','Pending','','{}')".format(LoggedInEmployeeID,LoggedInName,request,TimeStamp()))
                    cur.execute("INSERT into logs values('{}','{}','{}','{}','{}')".format(LoggedInEmployeeID,LoggedInName,'Submitted a Request',LoggedInName,TimeStamp()))
                    con.commit()
                    print('Request Submitted!')


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