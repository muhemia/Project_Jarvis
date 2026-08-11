import requests
import cv2
#from intern_modules.env import RENDER_API

def upload_pic(person, prob, frame):
    # default API to local backend
    API="http://localhost:8000/api/pic"
    
    # codiert den Tensor in NumPy-Array mit JPEG-kodierten Daten
    success, encoded_image = cv2.imencode(".jpg", frame)
    if not success:
        print("Fehler beim codieren des Bildes")
        return
    
    jpeg_bytes_image = encoded_image.tobytes()
    
    
    # files liest aus Arbeitsspeicher das Bild und schickt multipart/form-data statt Json
    files = {"image": 
        ("EMIR.jpg", jpeg_bytes_image, "image/jpeg")
    }
    
    response = requests.post(    
        API,
        files=files
    )

    print(f"PERSON IST {person} zu {prob*100}% UND WIRD NUN VERARBEITET!")
    print(response.json())
    
if __name__ == "__main__":
    pass