import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

image_path = "input_images/test1.jpeg"
image = cv2.imread(image_path)

if image is None:
    print("Error: Image load nahi ho payi. Path check karo.")
else:
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            print("Pose detect ho gaya! Landmarks mil gaye.")

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            output_path = "output_images/test1_pose.jpg"
            cv2.imwrite(output_path, image)
            print("Skeleton wali image save ho gayi:", output_path)

            important_points = [
                mp_pose.PoseLandmark.LEFT_SHOULDER,
                mp_pose.PoseLandmark.RIGHT_SHOULDER,
                mp_pose.PoseLandmark.LEFT_HIP,
                mp_pose.PoseLandmark.RIGHT_HIP,
            ]

            print("\n--- Important Landmarks ---")
            for point in important_points:
                landmark = results.pose_landmarks.landmark[point]
                print(f"{point.name}: x={landmark.x:.3f}, y={landmark.y:.3f}, visibility={landmark.visibility:.3f}")

            cv2.imshow("Pose Detection Result", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Koi pose detect nahi hua is image mein.")
