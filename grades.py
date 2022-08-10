# Program for interacting with a mySQL database
# Subject: Introduction Computer Programming Using Python
# Student: Aleksandr Tselikovskii

from mysql.connector import MySQLConnection, Error
from mySqlDbConfig import readDbConfig

def insertGrade(firstName, lastName, province, grade):
    try:
        dbconfig = readDbConfig()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        sql = "INSERT INTO Grades(FName,LName,Province,Grade) VALUES (%s, %s, %s, %s)"
        val = (firstName, lastName, province, grade)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "record inserted.")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return

def deleteGrade(firstName, lastName, province, grade):
    try:
        dbconfig = readDbConfig()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        sql = "DELETE FROM Grades WHERE FName = %s AND LName = %s AND Province = %s AND Grade = %s"
        val = (firstName, lastName, province, grade)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "record(s) deleted")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return

def displayGrade(firstName, lastName, province):
    try:
        listOfGrades = [] # list to save mysql query result
        dbconfig = readDbConfig()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        queryAlt = f"SELECT * FROM grades WHERE LName LIKE '%{lastName}%' AND FName LIKE '%{firstName}%' AND Province LIKE '%{province}%'"
        cursor.execute(queryAlt)
        row = cursor.fetchone()
        print('-' * 55)
        while row is not None:
            listOfGrades.append(row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3])
            spacesFname = 20 - len(row[0]) # counting the spaces to output the table properly in the terminal
            spacesLname = 20 - len(row[1])
            print('| ' + row[0] + ' ' * spacesFname + '| ', row[1] + ' ' * spacesLname +
                  '| ' + row[2] + ' | ' + row[3] + ' |')
            row = cursor.fetchone()
        print('-' * 55)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return listOfGrades

# generate and output an HTML code to the file
def getHTMLcode(listOfGrades):
    f = open("grade.html", 'w')
    f.write('<table border="1" style="border-collapse: collapse">\n')
    for row in listOfGrades:
        rowSplit = str(row).split() # splitting words/columns of a list element
        if len(rowSplit) == 4: # if we got a record with all fields/columns
            htmlLine = "<tr><td>" + rowSplit[0] + "</td><td>" + rowSplit[1] + "</td><td>" + rowSplit[2] + \
                       "</td><td>" + rowSplit[3] + "</td></tr>\n"

        else: # this part of code is only for cases, when user got a record with some empty fields
            htmlLine = '<tr>'
            for column in rowSplit:
                htmlLine = htmlLine + "<td>" + column + "</td>"
            htmlLine = htmlLine + '</tr>\n'

        f.write(htmlLine)
    f.write("</table>")
    print('\nHTML code is generated in the file "grade.html"')
    f.close()

def inputData(enterAllfields):
    firstName = input('Please, enter the first name > ')
    lastName = input('Please, enter the last name > ')
    province = input('Please, enter the province (e.g. ON, NB) > ')
    province = province.upper()
    if enterAllfields == True: # this part only for if user needs to enter all four parameters
        grade = input('Please, enter the grade > ')
        grade = grade.upper()
        return firstName, lastName, province, grade
    return firstName, lastName, province

if __name__ == '__main__':
    repeat = True
    while repeat:
        print('\nTest1. Interaction with a mySQL database\n' + '-' * 43)
        print('Enter 1 to INSERT a grade')
        print('Enter 2 to DISPLAY a grade')
        print('Enter 3 to DELETE a grade')
        print('Enter 4 to Exit')
        print('-' * 43)
        validation = False
        while validation == False:
            # Input data: integers from 1 to 5
            try:
                menuItem = input('Your choice > ')
                menuItem = int(menuItem)
                if 0 < menuItem <= 4:
                    if menuItem == 1:
                        firstName, lastName, province, grade = inputData(True)
                        insertGrade(firstName, lastName, province, grade)
                        validation = True
                    elif menuItem == 2:
                        firstName, lastName, province = inputData(False)
                        listOfGrades = displayGrade(firstName, lastName, province) # getting a result of query to database
                        getHTMLcode(listOfGrades)
                        validation = True
                    elif menuItem == 3:
                        firstName, lastName, province, grade = inputData(True)
                        deleteGrade(firstName, lastName, province, grade)
                        validation = True
                    else:
                        validation = True
                        repeat = False
                else:
                    print('Please type 1, 2, 3, or 4')
            except:
                print('Invalid input')
print('Have a nice day...')