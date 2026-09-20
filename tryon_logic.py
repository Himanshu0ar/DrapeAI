import cv2
import numpy as np
import mediapipe as mp
from rembg import remove
from PIL import Image

mp_pose = mp.solutions.pose

def run_tryon(person_path, garment_path, output_path):
    garment_nobg_path = "output_images/temp_garment_nobg.png"
    garment_image = Image.open(garment_path)
    garment_nobg = remove(garment_image)
    garment_nobg.save(garment_nobg_path)

    person_cv = cv2.imread(person_path)
    image_height, image_width, _ = person_cv.shape
    image_rgb = cv2.cvtColor(person_cv, cv2.COLOR_BGR2RGB)

    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(image_rgb)

        if not results.pose_landmarks:
            return False, "Pose detect nahi hua is image mein."

        landmarks = results.pose_landmarks.landmark
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

        ls = (int(left_shoulder.x * image_width), int(left_shoulder.y * image_height))
        rs = (int(right_shoulder.x * image_width), int(right_shoulder.y * image_height))
        lh = (int(left_hip.x * image_width), int(left_hip.y * image_height))
        rh = (int(right_hip.x * image_width), int(right_hip.y * image_height))

        shoulder_width = abs(rs[0] - ls[0])
        hip_width = abs(rh[0] - lh[0])
        garment_width = int(shoulder_width * 2.3)
        shoulder_avg_y = (ls[1] + rs[1]) // 2
        hip_avg_y = (lh[1] + rh[1]) // 2
        garment_height = int(abs(hip_avg_y - shoulder_avg_y) * 1.4)
        center_x = (ls[0] + rs[0]) // 2
        paste_x = center_x - garment_width // 2
        paste_y = shoulder_avg_y - int(garment_height * 0.22)

        garment_pil = Image.open(garment_nobg_path).convert("RGBA").resize((garment_width, garment_height))
        canvas = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
        canvas.paste(garment_pil, (paste_x, paste_y), garment_pil)
        canvas_np = np.array(canvas)

        source_pts = np.array([[
            [paste_x, paste_y],
            [paste_x + garment_width, paste_y],
            [paste_x, paste_y + garment_height],
            [paste_x + garment_width, paste_y + garment_height]
        ]], dtype=np.float32)

        top_half_width = int(shoulder_width * 1.15)
        bottom_half_width = int(hip_width * 1.15)
        target_pts = np.array([[
            [center_x - top_half_width, paste_y],
            [center_x + top_half_width, paste_y],
            [center_x - bottom_half_width, paste_y + garment_height],
            [center_x + bottom_half_width, paste_y + garment_height]
        ]], dtype=np.float32)

        matches = [cv2.DMatch(i, i, 0) for i in range(4)]
        tps = cv2.createThinPlateSplineShapeTransformer()
        tps.estimateTransformation(target_pts, source_pts, matches)
        warped = tps.warpImage(canvas_np)

        warped_pil = Image.fromarray(warped)
        person_pil = Image.open(person_path).convert("RGBA")
        person_pil.paste(warped_pil, (0, 0), warped_pil)
        person_pil.save(output_path)

        return True, "Success"
