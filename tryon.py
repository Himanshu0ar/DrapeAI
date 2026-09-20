import cv2
import mediapipe as mp
from rembg import remove
from PIL import Image

mp_pose = mp.solutions.pose

garment_path = "input_images/black-t-shirt.png"
garment_output_path = "output_images/garment_nobg.png"

garment_image = Image.open(garment_path)
garment_nobg = remove(garment_image)
garment_nobg.save(garment_output_path)

person_path = "input_images/test1.jpeg"
person_image = cv2.imread(person_path)
image_height, image_width, _ = person_image.shape
image_rgb = cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB)

with mp_pose.Pose(static_image_mode=True) as pose:
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

        left_shoulder_px = (int(left_shoulder.x * image_width), int(left_shoulder.y * image_height))
        right_shoulder_px = (int(right_shoulder.x * image_width), int(right_shoulder.y * image_height))
        left_hip_px = (int(left_hip.x * image_width), int(left_hip.y * image_height))
        right_hip_px = (int(right_hip.x * image_width), int(right_hip.y * image_height))

        shoulder_width_px = abs(right_shoulder_px[0] - left_shoulder_px[0])
        garment_width = int(shoulder_width_px * 2.3)

        shoulder_avg_y = (left_shoulder_px[1] + right_shoulder_px[1]) // 2
        hip_avg_y = (left_hip_px[1] + right_hip_px[1]) // 2
        garment_height = int(abs(hip_avg_y - shoulder_avg_y) * 1.4)

        garment_pil = Image.open(garment_output_path).convert("RGBA")
        garment_resized = garment_pil.resize((garment_width, garment_height))

        center_x = (left_shoulder_px[0] + right_shoulder_px[0]) // 2
        paste_x = center_x - garment_width // 2
        paste_y = shoulder_avg_y - int(garment_height * 0.22)

        person_pil = Image.open(person_path).convert("RGBA")
        person_pil.paste(garment_resized, (paste_x, paste_y), garment_resized)

        final_output_path = "output_images/final_tryon.png"
        person_pil.save(final_output_path)

        print("Try-on complete! Saved to:", final_output_path)
    else:
        print("Pose detect nahi hua.")
