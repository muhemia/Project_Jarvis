# Jarvis -- Intelligent Camera & Face Recognition System

Jarvis is a real-time camera monitoring system that detects and
identifies known persons using facial embeddings.

The system processes a live camera stream with **OpenCV**, detects faces
using **MTCNN**, and generates **512-dimensional face embeddings** using
a pretrained **InceptionResnetV1** model.

To prevent repeated notifications, Jarvis uses event-based detection
logic to track currently visible persons. A new notification is only
triggered when a person newly appears.

When a person is identified, the current camera frame is JPEG-encoded
directly in memory and sent via an HTTP `multipart/form-data` request to
a **Node.js / Express** backend.

The backend receives and processes the image in memory using **Multer**,
converts the image data to Base64, and forwards it through the **Brevo
REST API**. An email notification containing the captured image is then
sent automatically.

The backend is deployed as a cloud service on **Render**, while API keys
and other sensitive configuration are managed using environment
variables.

## Architecture

```text
Camera
  ↓
OpenCV
  ↓
MTCNN Face Detection
  ↓
InceptionResnetV1 Embedding
  ↓
Face Identification
  ↓
Event Detection
  ↓
JPEG Encoding (in-memory)
  ↓
HTTP / multipart-form-data
  ↓
Node.js + Express + Multer
  ↓
Brevo REST API
  ↓
Email Notification
```

## Tech Stack

- **Python**
- **OpenCV**
- **PyTorch**
- **facenet-pytorch**
- **NumPy**
- **Node.js**
- **Express**
- **Multer**
- **REST / HTTP**
- **Brevo API**
- **Render**

## Key Features

- Real-time camera processing
- Face detection and identification
- Face recognition based on 512-dimensional embeddings
- Event-based notification logic to prevent repeated alerts
- In-memory JPEG encoding without temporary image files
- Image upload using `multipart/form-data`
- Node.js / Express REST backend
- In-memory file handling with Multer
- Automated email notifications with image attachments
- Cloud-hosted backend
- Secure configuration through environment variables
