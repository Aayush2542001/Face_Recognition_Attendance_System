import cv2
import face_recognition
import os
import pickle

AayushEncode, ArthEncode, KayuEncode, SnehalEncode = [], [], [], []

def loadLocally(locally):
    PEOPLE = os.getcwd() + "\\" + "PEOPLE"
    if locally:
        for person in os.listdir(PEOPLE):
            File = open(os.getcwd() + "\\Pickle\\EncodeObjects\\" + person + "Encode.pickle", 'wb')
            pickle.dump(globals()[person + "Encode"], File)
            File.close()
    else:
        for person in os.listdir(PEOPLE):
            File = open(os.getcwd() + "\\Pickle\\EncodeObjects\\" + person + "Encode.pickle", 'rb')
            globals()[person + "Encode"] = pickle.load(File)
            File.close()

def testFolderImage():
    testDir = os.getcwd() + "\\" + "Test"
    for imageName in os.listdir(testDir):
        IMG = face_recognition.load_image_file(str(testDir) + "\\" + str(imageName))
        encode = face_recognition.face_encodings(IMG)
        if len(encode):
            dis1 = face_recognition.face_distance(aayushEncode, encode[0])
            dis2 = face_recognition.face_distance(arthEncode, encode[0])
            dis3 = face_recognition.face_distance(snehalEncode, encode[0])
            dis1 = sum(dis1)/len(dis1)
            dis2 = sum(dis2) / len(dis2)
            dis3 = sum(dis3) / len(dis3)
            if min(dis1,dis2,dis3) == dis1:
                print("Aayush")
            elif min(dis1,dis2,dis3) == dis2:
                print("Arth")
            else:
                print("Snehal")
        else:
            print("Face not found in "+imageName)


def testFrame(frame):
    while True:
        frameEncode = face_recognition.face_encodings(frame)
        minDistance, minPerson = 1.0, "XXX"
        PEOPLE = os.getcwd() + "\\" + "PEOPLE"

        if len(frameEncode):
            for person in os.listdir(PEOPLE):
                distances = face_recognition.face_distance(globals()[person + "Encode"], frameEncode[0])
                average = sum(distances) / len(distances)
                if average < minDistance:
                    minDistance = average
                    minPerson = person
            return minPerson, str(minDistance)
        else:
            return "No person in Frame", "0"

def captureFromWebCame():
    # no need to save image and then load
    loadLocally(False)
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        noError, capture = camera.read()

        encode = face_recognition.face_encodings(capture)
        if len(encode):
            dis1 = face_recognition.face_distance(aayushEncode, encode[0])
            dis2 = face_recognition.face_distance(arthEncode, encode[0])
            dis3 = face_recognition.face_distance(kayuEncode, encode[0])
            dis4 = face_recognition.face_distance(snehalEncode, encode[0])
            dis1 = sum(dis1) / len(dis1)
            dis2 = sum(dis2) / len(dis2)
            dis3 = sum(dis3) / len(dis3)
            dis4 = sum(dis4) / len(dis4)
            cv2.putText(capture,str(dis1),(30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(capture, str(dis2), (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(capture, str(dis3), (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(capture, str(dis4), (30,140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Camera', capture)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

def trainAndEncode():
    PEOPLE = os.getcwd() + "\\" + "PEOPLE"
    for person in os.listdir(PEOPLE):
        for imageName in os.listdir(PEOPLE + '\\' + person):
            simpleImage = face_recognition.load_image_file(PEOPLE + "\\" + person + "\\" + imageName)
            simpleImage = cv2.cvtColor(simpleImage, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(simpleImage)
            if len(encode):
                globals()[person+"Encode"].append(encode[0])
            else:
                print("Face not found in " + imageName)
    loadLocally(True)


if __name__ == "__main__":
    trainAndEncode()
    # captureFromWebCame()
