# SafeHouse Project

This is a Python project that includes:
- SQLite database for data storage
- Backend API (FastAPI)
- Frontend web interface
- AI processing for images from web-camera
- Laser controllers

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the backend: `uvicorn backend.app:app --reload`
3. Open frontend in browser

## Features

- Database: SQLite for storing data
- Backend: FastAPI for API endpoints
- Frontend: Simple HTML/JS interface
- AI: Image processing using OpenCV and a pre-trained model
- Lasers: Control via serial communication