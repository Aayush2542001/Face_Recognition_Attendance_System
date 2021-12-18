# PRAGMA table_info(Name)
# table schema

# INSERT INTO Name(name) VALUES('Aayush')
# INSERT INTO Name(id, name) VALUES(4, 'Arth') # increment will continue from 4
# Insert into Name

# result = cursor.fetchall()
# print(result)
# prints result of last cursor.execute()


import sqlite3
from datetime import datetime
import inspect
import Functions

connection = None
cursor = None
USER_TABLE = "Name"
ATTENDANCE_TABLE = "Attendance"

class Database:
    @staticmethod
    def constructor():
        global cursor, connection
        # connection
        connection = sqlite3.connect("FaceRecognition.db")
        cursor = connection.cursor()
        # cursor.execute("UPDATE Name SET isWorking = 0")
        # Database.commit()

    @staticmethod
    def createTables():
        # creating tables if not exist
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {USER_TABLE}(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, isWorking BOOLEAN)")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {ATTENDANCE_TABLE}(id INTEGER, mydate DATETIME, startJob BOOLEAN)")
        Database.commit()

    @staticmethod
    def addEmployee(empName):
        global cursor
        cursor.execute(f"INSERT INTO {USER_TABLE}(name,isWorking) VALUES('{empName}',0)")
        Database.commit()
        return cursor.execute(f"select seq from sqlite_sequence where name={USER_TABLE}").fetchall()[0][0]
        # returns last entry's id of MAIN_TABLE

    @staticmethod
    def addAttendance():
        global cursor
        cursor.execute(f"Insert into {ATTENDANCE_TABLE} VALUES(1,'2021-08-20 12:00:00',1)")
        cursor.execute(f"Insert into {ATTENDANCE_TABLE} VALUES(1,'2021-08-20 16:00:00',0)")
        cursor.execute(f"Insert into {ATTENDANCE_TABLE} VALUES(1,'2021-08-20 17:00:00',1)")
        cursor.execute(f"Insert into {ATTENDANCE_TABLE} VALUES(1,'2021-08-20 19:00:00',0)")
        cursor.execute(f"Insert into {ATTENDANCE_TABLE} VALUES(2,'2021-08-21 12:00:00',1)")
        cursor.execute(f"Insert into {ATTENDANCE_TABLE} VALUES(2,'2021-08-21 14:00:00',0)")
        Database.commit()

    @staticmethod
    def attendance(detectedPerson):
        # getting Id and isWorking and cur_time for INSERT query
        dateFormat = "%Y-%m-%d %H:%M:%S"
        Id,isWorking = Database.getIdWorkingByName(detectedPerson)
        cur_time = datetime.today().strftime(dateFormat)

        # getting lastAttendance info to check if user given attendance in last 5 minutes
        LastId, LastMyDate = Database.lastAttendance()
        if Id == LastId:
            timeDifference = datetime.strptime(cur_time, dateFormat) - datetime.strptime(LastMyDate, dateFormat)
            if (timeDifference.total_seconds())/60 < 3:  # it won't take attendance again within 3 minutes for same person
                return LastMyDate

        # taking attendance
        isWorking = not isWorking
        cursor.execute(f"UPDATE {USER_TABLE} SET isWorking = {int(isWorking)} WHERE id = {Id}")
        cursor.execute(f"INSERT INTO {ATTENDANCE_TABLE} VALUES({Id},'{cur_time}',{int(isWorking)})")
        Database.commit()
        return datetime.strptime(cur_time, dateFormat).strftime("%H:%M:%S")  # returning cur_time(HH:MM:SS)

    @staticmethod
    def getIdWorkingByName(detectedPerson):
        global cursor

        # getting Id and isWorking from table
        result = cursor.execute(f"Select id,isWorking from {USER_TABLE} WHERE name = '{detectedPerson}'")
        ResultList = result.fetchall()
        return ResultList[0][0],ResultList[0][1]

    @staticmethod
    def lastAttendance():
        global cursor

        result = cursor.execute(f"SELECT id, mydate FROM {ATTENDANCE_TABLE}")
        ResultList = result.fetchall()
        if len(ResultList):  # returning last attendance info if exists
            return ResultList[-1][0], ResultList[-1][1]
        else:
            return -1,""

        # ResultList[0][2] is giving 0 value bcz of "ORDER BY mydate"
        # solution: get * from Attendance_table and take last row manually

    @staticmethod
    def dropTable(tableName):
        global cursor

        cursor.execute(f"DROP TABLE IF EXISTS {tableName}")
        Database.commit()

    @staticmethod
    def deleteRecords(tableName):
        global cursor

        cursor.execute(f"DELETE FROM {tableName}")
        Database.commit()

    @staticmethod
    def printTable(tableName):
        global cursor
        result = cursor.execute(f"SELECT * FROM {tableName}")
        for row in result.fetchall():
            print(row[0], " ", row[1])

    @staticmethod
    def getNames():
        global cursor

        result = cursor.execute(f"SELECT name FROM {USER_TABLE}")
        returnList = []
        for row in result:
            returnList.append(row[0])
        return returnList

    @staticmethod
    def getIdNames():
        global cursor
        result = cursor.execute(f"SELECT * FROM {USER_TABLE}")
        returnList = []
        for row in result:
            returnList.append([str(row[0]), row[1]])
        return returnList

    @staticmethod
    def updateById(idToUpdate,updatedName):
        global cursor
        cursor.execute(f"UPDATE {USER_TABLE} SET name = '{updatedName}' WHERE id = {idToUpdate}")
        connection.commit()

    @staticmethod
    def deleteById(idToDelete):
        global cursor
        cursor.execute(f"DELETE FROM {USER_TABLE} WHERE id = {idToDelete}")
        connection.commit()

    @staticmethod
    def presentTables():
        global cursor
        result = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        print(result.fetchall())

    @staticmethod
    def commit():
        global connection
        connection.commit()

    @staticmethod
    def getWorkedTimeManually(startDate, endDate):
        global cursor

        # getting last registered id(Total employees)
        LastId = cursor.execute(f"SELECT seq from sqlite_sequence WHERE name = {USER_TABLE}").fetchall()[0][0]

        dateFormat = "%Y-%m-%d %H:%M:%S"
        IdNameDict = Functions.ListToDictionary(Database.getIdNames())
        returnList = []

        # getting attendance record for each id
        for i in range(1, LastId+1):
            resultList = cursor.execute(f"SELECT mydate,startJob from {ATTENDANCE_TABLE} WHERE id = {i} and mydate BETWEEN '{startDate}' AND '{endDate}'").fetchall()

            # subtracting endJob - startJob and storing in workedSeconds
            workedSeconds = 0
            for row1, row2 in zip(resultList[0::2], resultList[1::2]):
                timeDifference = datetime.strptime(row2[0], dateFormat) - datetime.strptime(row1[0], dateFormat)
                workedSeconds += timeDifference.total_seconds()

            # converting workedSeconds to HH:MM:SS format
            HH, MM = divmod(workedSeconds, 3600)
            MM, SS = divmod(MM, 60)
            convertedDate = '{:02}:{:02}:{:02}'.format(int(HH), int(MM), int(SS))

            # appending result
            # maybe error for deleted employee
            returnList.append([str(i),IdNameDict[i],convertedDate])

        return returnList

    @staticmethod
    def getWorkedTime():
        global cursor
        result = cursor.execute("""
WITH cte AS (
  SELECT *, SUM(startJob) OVER (PARTITION BY id ORDER BY mydate) grp
  FROM Attendance
)
SELECT DISTINCT u.id, u.name,  
       TIME(SUM(strftime('%s', MAX(c.mydate)) - strftime('%s', MIN(c.mydate))) OVER (PARTITION BY u.id), 'unixepoch') timeDifferenceInHours
FROM Name u LEFT JOIN cte c
ON c.id = u.id
GROUP BY u.id, c.grp;
        """)
        # for row in result.fetchall():
        #     print(row)
        return result.fetchall()

# essential statement to initialize global variables
Database.constructor()

# no other statements should present here
# execute from webcam file