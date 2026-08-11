# Jarvis — Intelligent Camera & Face Recognition System

Jarvis is a real-time smart camera system that identifies known persons and automatically sends image-based email notifications when a person newly appears in front of the camera.

The application combines computer vision, deep-learning-based face embeddings, event detection, a Python desktop interface, and a cloud-hosted Node.js backend.

## Demo

<!-- Add a short demo video or GIF here -->

## How It Works

The live camera stream is processed with **OpenCV**. Faces are detected using **MTCNN** and converted into **512-dimensional embeddings** using a pretrained **InceptionResnetV1** model.

These embeddings are compared against stored reference embeddings to identify known persons.

Jarvis keeps track of currently visible persons so that notifications are only triggered when somebody newly enters the camera view.

When an event occurs, the current camera frame is JPEG-encoded directly in memory and uploaded via HTTP `multipart/form-data` to a cloud-hosted **Node.js / Express** backend.

The backend receives and processes the uploaded image in memory using **Multer**, converts the image data to Base64, and forwards it through the **Brevo REST API**.

An automated email notification containing the captured image is then sent.

The backend is deployed on **Render**, while API keys and other sensitive configuration are managed using environment variables.

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

## Application Flow

1. Launch the Jarvis desktop application.
2. Start the camera through the CustomTkinter interface.
3. Jarvis detects faces in the live camera stream.
4. Facial embeddings are generated and compared against the local face database.
5. Newly detected known persons trigger an event.
6. The current camera frame is JPEG-encoded in memory.
7. The image is uploaded to the backend using `multipart/form-data`.
8. The backend processes the image using Multer.
9. The backend calls the Brevo REST API.
10. An email notification containing the captured image is sent automatically.

## Tech Stack

### Client / Computer Vision

- **Python**
- **CustomTkinter**
- **OpenCV**
- **PyTorch**
- **facenet-pytorch**
- **NumPy**
- **MTCNN**
- **InceptionResnetV1**

### Backend

- **Node.js**
- **Express**
- **Multer**
- **REST / HTTP**
- **multipart/form-data**
- **Brevo API**

### Deployment

- **Render**
- **Environment Variables**

## Key Features

- Real-time camera processing
- Desktop interface built with CustomTkinter
- Face detection and identification
- Face recognition based on 512-dimensional embeddings
- Comparison against stored reference embeddings
- Event-based notification logic to prevent repeated alerts
- Tracking of currently visible persons
- In-memory JPEG encoding without temporary image files
- Image upload using `multipart/form-data`
- Node.js / Express REST backend
- In-memory file handling with Multer
- Automated email notifications with image attachments
- Cloud-hosted backend
- Secure configuration through environment variables

## Project Structure

The exact file names may vary, but the project is separated into a Python client and a Node.js backend.

```text
Project_Jarvis/
├── Jarvis/
│   ├── main.py
│   ├── frontend.py
│   ├── face_db.pt          # local only / not committed
│   └── ...
│
└── Backend/
    ├── server.js
    ├── ...
    └── .env                # local only / not committed
```

## Running the Project

### Python Client

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install the required Python dependencies:

```bash
pip install customtkinter opencv-python torch torchvision facenet-pytorch numpy
```

Start Jarvis from the Python project directory:

```bash
python3 -m main
```

### Backend

Install the Node.js dependencies:

```bash
npm install
```

Start the backend locally:

```bash
node server.js
```

For the deployed version, configure the required environment variables in the hosting environment.

## Face Database

Jarvis identifies known persons by comparing live facial embeddings against previously stored reference embeddings.

The local face database contains personal biometric data and is therefore not included in the repository.

Users should generate their own reference embeddings before running face identification.

## Privacy & Security

Personal face embeddings, captured images, and API credentials are not included in this repository.

Sensitive files such as the following should be excluded using `.gitignore`:

```text
.env
face_db.pt
Pictures/
__pycache__/
.venv/
node_modules/
```

API keys and other secrets should be stored in environment variables rather than directly in the source code.

## Notes

The face recognition model is not trained from scratch. Jarvis uses a pretrained **InceptionResnetV1** model and performs identification by comparing the generated face embeddings against stored reference embeddings.

This project focuses on integrating real-time computer vision, event-based application logic, backend communication, cloud deployment, and automated notification delivery into one end-to-end system.
