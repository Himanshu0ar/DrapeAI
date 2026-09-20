# DrapeAI - Real-Time Virtual Try-On & Garment Mapping Engine

AI-powered Virtual Try-On (VTON) system that lets a user upload a photo and see a selected garment realistically overlaid onto their own body - adjusted for pose and body shape.

## Problem
Online apparel shopping has high return rates (30-40%) due to poor fit and unmet visual expectations. This project builds a progressive, learning-focused MVP toward solving that.

## Tech Stack
- Python
- OpenCV
- MediaPipe (Pose Estimation)
- rembg / U2Net-based model (Segmentation)
- PyTorch (for future warping phase)
- FastAPI (planned - backend)
- React (planned - frontend)

## Phases

| Phase | Status | Description |
|---|---|---|
| 1. Pose Estimation | Done | Detect 33 body landmarks using MediaPipe |
| 2. Segmentation | Done | Remove background, generate person mask using rembg |
| 3. Basic 2D Try-On | Upcoming | Overlay garment aligned to body using pose data |
| 4. Deep Warping | Upcoming | Realistic cloth deformation |
| 5. Real-Time Webcam | Upcoming | Live try-on |
| 6. Web App + Deployment | Upcoming | Full product with UI |

## How to Run

Activate virtual environment: venv\Scripts\activate
Run pose estimation: python pose_estimation.py
Run segmentation: python segmentation.py

## Project Structure

DrapeAI/
- input_images/       Test photos
- output_images/      Results (pose overlays, masks, segmented images)
- pose_estimation.py  Phase 1: Pose detection
- segmentation.py     Phase 2: Background removal + masking
