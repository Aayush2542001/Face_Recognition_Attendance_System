import face_recognition
import os
import pickle
from Database import *
import time

CWD = os.getcwd()
minPersonPath = CWD + "\\Pickle\\FaceDetectObjects\\minPerson.pickle"
encodeObjectPath = CWD + "\\Pickle\\EncodeObjects\\"

def write(path,data):
    try:
        File = open(path, 'wb')
        pickle.dump(data, File)
        File.close()
    except:
        print(f"Error writing file:{os.path.basename(path)}")

def read(path):
    try:
        File = open(path, 'rb')
        data = pickle.load(File)
        File.close()
        return data
    except:
        # error
        print(path)
        print(f"Error reading file:{os.path.basename(path)}")

def ListToDictionary(List):
    Dict = {}
    for row in List:
        Dict[int(row[0])] = row[1]
    return Dict

def testFrameProcess():
    PEOPLE = Database.getNames()
    if len(PEOPLE) == 0:
        write(minPersonPath,"No employees available")

    # getting encodes from local storage to list
    for person in PEOPLE:
        globals()[person + "Encode"] = read(encodeObjectPath + person + "Encode.pickle")

    # comparing captured frame with encodes and storing minPerson in pickle
    while True:
        try:
            frameEncode = face_recognition.face_encodings(read(CWD + "\\Pickle\\FaceDetectObjects\\frame.pickle"))
        except:
            continue

        minDistance = 200
        if len(frameEncode):
            for person in PEOPLE:
                distances = face_recognition.face_distance(globals()[person + "Encode"], frameEncode[0])
                average = sum(distances) / len(distances)
                if average < minDistance:
                    minDistance = average
                    write(minPersonPath,person)
        else:
            write(minPersonPath,"Scanning mode")
        time.sleep(1)

def saveEncodes(empName,EncodeList):
    write(encodeObjectPath + empName + "Encode.pickle",EncodeList)

def updateEncodes(empName,updatedEncode):
    write(encodeObjectPath + empName + "Encode.pickle",updatedEncode)

def deleteEncode(encodeToDelete):
    os.remove(encodeObjectPath + encodeToDelete + "Encode.pickle")

def updateEncodeFileName(oldName,updatedName):
    os.rename(encodeObjectPath + oldName + "Encode.pickle", encodeObjectPath + updatedName + "Encode.pickle")

