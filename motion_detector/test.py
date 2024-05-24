import time

import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats import landmark_pb2


class landmarker_and_result():
    def __init__(self):
        self.result = mp.tasks.vision.PoseLandmarkerResult
        self.landmarker = mp.tasks.vision.PoseLandmarker
        self.createLandmarker()

    def createLandmarker(self):
        def update_result(result: mp.tasks.vision.PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
            self.result = result
        options = mp.tasks.vision.PoseLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path="../pose_landmarker_full.task"),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            result_callback=update_result)

        self.landmarker = self.landmarker.create_from_options(options)

    def detect_async(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.landmarker.detect_async(image=mp_image, timestamp_ms=int(time.time() * 1000))

    def close(self):
        self.landmarker.close()


def draw_landmarks_on_image(rgb_image, detection_result: mp.tasks.vision.PoseLandmarkerResult):
    print(detection_result)
    try:
        if detection_result.pose_landmarks == []:
            return rgb_image
        else:
            pose_landmarks_list = detection_result.pose_landmarks
            pose_world_landmarks_list = detection_result.pose_world_landmarks
            annotated_image = np.copy(rgb_image)

            for idx in range(len(pose_landmarks_list)):
                pose_landmarks = pose_landmarks_list[idx]

                hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                hand_landmarks_proto.landmark.extend([
                    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in
                    pose_landmarks])
                mp.solutions.drawing_utils.draw_landmarks(
                    annotated_image,
                    hand_landmarks_proto,
                    mp.solutions.pose.POSE_CONNECTIONS,
                    mp.solutions.drawing_styles.get_default_pose_landmarks_style())

            return annotated_image
    except:
        return rgb_image

hand_landmarker = landmarker_and_result()
cap = cv2.VideoCapture(0)

while True:
    # pull frame
    ret, frame = cap.read()
    # mirror frame
    frame = cv2.flip(frame, 1)
    # update landmarker results
    hand_landmarker.detect_async(frame)
    frame = draw_landmarks_on_image(frame, hand_landmarker.result)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# release everything
hand_landmarker.close()
cap.release()
cv2.destroyAllWindows()

