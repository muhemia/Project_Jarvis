import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from pathlib import Path


# param File with .jpg files
# create embeddings of persons you want to detect 
# stores them in a lokal file `face_db.pt`
def create_faces_db():
    base_path = Path("intern_modules/Pics")
    mtcnn = MTCNN()
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    
    face_db = {}
    
    for person_pic in base_path.iterdir():
        frame = cv2.imread(str(person_pic))
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        face = mtcnn(frame)
        
        face = face.unsqueeze(0)

        with torch.no_grad():
            embedding = resnet(face)
        
        face_db[str(person_pic.stem)] = embedding
        
    for person_name in face_db.keys():
        print(f"Personen: {person_name}")
        
    print("Wurden initialisiert!")
    torch.save(face_db, "face_db.pt")


if __name__=="__main__":        
    create_faces_db()