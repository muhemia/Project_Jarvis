import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from intern_modules.api2backend import upload_pic
from intern_modules.createFaceDB import create_faces_db

import time

def main():
    print("MAIN HAT GESTARTET")
    mtcnn = MTCNN(keep_all=True)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    camera = cv2.VideoCapture(0)
    
    active_persons = {} # Personen die sich unmittelbar vor der Kamera befinden
    ABSCENT_TIME = 5 # Sekunden warten bis erneut ein Bild gemacht wird
    
    create_faces_db
    face_db = torch.load("face_db.pt")
    while True:
        now = time.time()
        success, bgr_frame = camera.read() # liest ein bild von der kamera ein: success ist ein boolean, frame ist das bild
        # FRAME IST EIN NUMPY ARRAY MIT DEN PIXELN DES BILDES
        # -> daher später in Bytes codieren um als Datei speichern zu können
        
        if not success:
            print("Fehler beim Lesen des Kamerabildes")
            break
        
        bgr_frame = cv2.flip(bgr_frame, 1) # spiegelt das bild horizontal
        
        frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB) # wandelt das bild von BGR in RGB um
        boxes, probabilistic = mtcnn.detect(frame) # erkennt gesichter im bild
        
        
        if boxes is not None:
            face_in_frame = mtcnn(frame) # -> macht daraus direkt nx3x160x160 Tensor
            
            with torch.no_grad():
                embedding = resnet(face_in_frame)
                
            lowest_dist = 1 #threshold
            name_of_person="unknown"
            for person, em in face_db.items():
                distance = torch.dist(em, embedding).item() # Abstand als float
                if distance < lowest_dist:
                    lowest_dist = distance
                    name_of_person=person
            
            
                  
            for box, prob in zip(boxes, probabilistic):
                cv2.rectangle(
                    bgr_frame,
                    (int(box[0]), int(box[1])),      # linke obere Ecke
                    (int(box[2]), int(box[3])),      # rechte untere Ecke
                    (255, 255, 255),     # Farbe in BGR
                    5           # Linienbreite
                )
                cv2.putText(bgr_frame, f"Es ist zu:{(prob)*100:.2f}% die Person: {name_of_person}", (int(box[0]), int(box[1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
        
            if name_of_person!="unknown" and probabilistic >= 0.9999:
                if not name_of_person in active_persons.keys():
                    active_persons[name_of_person] = now
                    print(f"{name_of_person} JETZT IN LISTE")
                    upload_pic(name_of_person, probabilistic, bgr_frame)
            
            for person, last_seen in list(active_persons.items()):
                if now - last_seen > ABSCENT_TIME:
                    del active_persons[person]
                    print(f"{person} DELETETTT")
                #break
        cv2.imshow("Kamerabild", bgr_frame) # zeigt das bild in einem fenster an
        
        pressed_key = cv2.waitKey(1) # wartet auf eine taste, bevor das fenster geschlossen wird
        
        
        # Taste s -> speichert das bild als testbild.jpg
        if pressed_key == ord("s"):
            cv2.imwrite("Pictures/testbild.jpg", frame)
            print("Bild gespeichert")
        
        # Taste q beendet das Programm
        if pressed_key == ord("q"):
            break
        
    camera.release() # gibt die kamera wieder frei
    cv2.destroyAllWindows() # schließt alle fenster
    
if __name__=="__main__":
    main()