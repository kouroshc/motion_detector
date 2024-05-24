import mediapipe as mp
import cv2

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
import numpy as np

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# @markdown To better demonstrate the Pose Landmarker API, we have created a set of visualization tools that will be used in this colab. These will draw the landmarks on a detect person, as well as the expected connections between those markers.
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import time


class Mediapipe_BodyModule:
    def __init__(self):
        self.mp_drawing = solutions.drawing_utils
        self.mp_pose = solutions.pose
        self.results = None

    def draw_landmarks_on_image(self, rgb_image, detection_result):
        pose_landmarks_list = detection_result.pose_landmarks
        # pose_landmarks_list = detection_result
        annotated_image = np.copy(rgb_image)

        # Loop through the detected poses to visualize.
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend(
                [
                    landmark_pb2.NormalizedLandmark(
                        x=landmark.x, y=landmark.y, z=landmark.z
                    )
                    for landmark in pose_landmarks
                ]
            )
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style(),
            )
        return annotated_image

    # Create a pose landmarker instance with the live stream mode:
    def print_result_face(
        self, result: FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int
    ):
        # print('face landmarker result: {}'.format(result))
        self.results = result
        # print(timestamp_ms)

    def main(self):
        option_face = FaceLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path="face_landmarker.task",
                delegate=python.BaseOptions.Delegate.GPU,
            ),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.print_result_face,
        )

        video = cv2.VideoCapture(0)

        timestamp = 0
        with FaceLandmarker.create_from_options(option_face) as landmarker_face:

            # The landmarker is initialized. Use it here.
            # ...
            while video.isOpened():
                # Capture frame-by-frame
                ret, frame = video.read()


                if not ret:
                    print("Ignoring empty frame")
                    # break

                timestamp += 1
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                landmarker_face.detect_async(mp_image, timestamp)

        video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    body_module = Mediapipe_BodyModule()
    body_module.main()