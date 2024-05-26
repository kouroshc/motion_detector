import logging
import os
import time
from datetime import datetime

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import math
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Detect:

    timeframe = 1
    output_folder = ''
    cap = cv2.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    angles_chart_time_value = {'left_knee_list': [],
                               'left_elbow_list': [],
                               'left_wrist_list': [],
                               'left_shoulder_list': [],
                               'right_knee_list': [],
                               'right_elbow_list': [],
                               'right_wrist_list': [],
                               'right_shoulder_list': []}
    angles_time_value = {'time': '',
                         'angles': []}
    angles_csv = []
  

    @classmethod
    def capture_image(cls):
        ret, frame = cls.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            return frame
        return None

    @classmethod
    def display_image(cls, frame):
        cv2.imshow('Camera Output', frame)

    @classmethod
    def caputre_image(cls):
        with cls.mp_pose.Pose(min_detection_confidence=.5, min_tracking_confidence=.5, smooth_landmarks=True) as pose:
            frame = cls.capture_image()
            results = pose.process(frame)
            annotated_image = frame.copy()
            cls.mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, cls.mp_pose.POSE_CONNECTIONS)
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + cls.send_image(annotated_image) + b'\r\n')

    @classmethod
    def buffer_image_for_web(cls):
        while True:
            start_time = time.time()
            frame = cls.capture_image()
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + cls.send_image(frame) + b'\r\n')
            else:
                break

            elapsed_time = time.time() - start_time
            logging.debug(f"Frame generation time: {elapsed_time} seconds")

    @classmethod
    def buffer_res_annotated_for_web(cls):
        with cls.mp_pose.Pose(min_detection_confidence=.5, min_tracking_confidence=.5, smooth_landmarks=True) as pose:
            while True:
                start_time = time.time()
                frame = cls.capture_image()
                # image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame)
                annotated_image = frame.copy()
                cls.mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, cls.mp_pose.POSE_CONNECTIONS)
                if frame is not None:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + cls.send_image(annotated_image) + b'\r\n')
                else:
                    break
                elapsed_time = time.time() - start_time
                logging.debug(f"Frame generation time: {elapsed_time} seconds")

    @classmethod
    def write_and_download(cls,status):
        with cls.mp_pose.Pose(min_detection_confidence=.5, min_tracking_confidence=.5, smooth_landmarks=False) as pose:
            folder_count = 1
            while True:
                cls.output_folder = f'stat\session_{folder_count}'
                print(cls.output_folder)
                if os.path.exists(cls.output_folder):
                    folder_count +=1
                if not os.path.exists(cls.output_folder):
                    os.mkdir(cls.output_folder)
                    break
            while True:
                frame = cls.capture_image()
                # image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame)
                annotated_image = frame.copy()
                cls.csv_pose_landmarks(results)
                frame_filename = os.path.join(cls.output_folder, f'frame_{str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))}.jpg')
                cls.mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, cls.mp_pose.POSE_CONNECTIONS)
                cv2.imwrite(frame_filename, annotated_image)
                if status == 'stop':
                    cls.make_excel(cls.output_folder)
                    cls.release_camera()

                time.sleep(cls.timeframe)

    @classmethod
    def buffer_res_empty_for_web(cls):
        with cls.mp_pose.Pose(min_detection_confidence=.5, min_tracking_confidence=.5, smooth_landmarks=True) as pose:
            while True:
                start_time = time.time()
                frame = cls.capture_image()
                # image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame)
                annotated_image = np.zeros_like(frame)
                cls.mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, cls.mp_pose.POSE_CONNECTIONS)
                if frame is not None:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + cls.send_image(annotated_image) + b'\r\n')
                else:
                    break

                elapsed_time = time.time() - start_time
                logging.debug(f"Frame generation time: {elapsed_time} seconds")

    @classmethod
    def send_image(cls, image):
        success, buffer = cv2.imencode('.jpg', image)
        generated_image = buffer.tobytes()
        return generated_image

    @classmethod
    def release_camera(cls):
        cls.cap.release()
        cv2.destroyAllWindows()

    @classmethod
    def pose_landmarks(cls, results):
        if results.pose_landmarks:
            # for landmark in results.pose_landmarks.landmark:
            joints_angles = [cls.left_elbow(results),
                             cls.right_elbow(results),
                             cls.right_shoulder(results),
                             cls.left_shoulder(results),
                             cls.right_knee(results),
                             cls.left_knee(results),
                             cls.right_wrist(results),
                             cls.left_wrist(results)]
            return joints_angles
    @classmethod
    def csv_pose_landmarks(cls, results):
        if results.pose_landmarks:
            # for landmark in results.pose_landmarks.landmark:
            cls.angles_time_value['time'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            cls.angles_time_value['angles'] = [cls.left_elbow(results),
                                               cls.right_elbow(results),
                                               cls.right_shoulder(results),
                                               cls.left_shoulder(results),
                                               cls.right_knee(results),
                                               cls.left_knee(results),
                                               cls.right_wrist(results),
                                               cls.left_wrist(results)]
            cls.angles_csv.append(cls.angles_time_value)
            cls.angles_time_value = {}

    @classmethod
    def right_elbow(cls, results):

        right_shoulder = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_WRIST]
        angle = cls.calculate_angle(right_wrist, right_elbow, right_shoulder, "آرنج چپ", 'right_elbow')

        return angle


    @classmethod
    def left_elbow(cls, results):
        left_shoulder = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_WRIST]
        angle = cls.calculate_angle(left_shoulder, left_elbow, left_wrist, "آرنج راست", 'left_elbow')

        return angle


    @classmethod
    def right_shoulder(cls, results):
        left_elbow = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_ELBOW]
        left_shoulder = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_hip = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_HIP]
        angle = cls.calculate_angle(left_elbow, left_shoulder, left_hip, "شانه راست", 'right_shoulder')

        return angle


    @classmethod
    def left_shoulder(cls, results):
        right_hip = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_HIP]
        right_shoulder = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_ELBOW]
        angle = cls.calculate_angle(right_hip, right_shoulder, right_elbow, "شانه چپ", 'left_shoulder')

        return angle


    @classmethod
    def right_knee(cls, results):
        left_hip = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_HIP]
        left_knee = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_KNEE]
        left_ankle = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_ANKLE]
        angle = cls.calculate_angle(left_ankle, left_knee, left_hip, "زانو راست", 'right_knee')

        return angle


    @classmethod
    def left_knee(cls, results):
        right_hip = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_HIP]
        right_knee = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_KNEE]
        right_ankle = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_ANKLE]
        angle = cls.calculate_angle(right_hip, right_knee, right_ankle, "زانو چپ", 'left_knee')

        return angle


    @classmethod
    def left_wrist(cls, results):
        right_thumb = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_THUMB]
        right_wrist = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_WRIST]
        right_pinky = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.RIGHT_PINKY]
        angle = cls.calculate_angle(right_pinky, right_wrist, right_thumb, "مچ چپ", 'right_wrist')
        return angle


    @classmethod
    def right_wrist(cls, results):
        left_thumb = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_THUMB]
        left_wrist = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_WRIST]
        left_pinky = results.pose_landmarks.landmark[cls.mp_pose.PoseLandmark.LEFT_PINKY]
        angle = cls.calculate_angle(left_thumb, left_wrist, left_pinky, "مچ راست", 'left_wrist')
        return angle


    @classmethod
    def calculate_angle(cls, a, b, c, part_name, part_name_list):
        angle_rad = math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x)
        angle_deg = math.degrees(angle_rad)
        angle_deg = angle_deg + 360 if angle_deg < 0 else angle_deg
        angle_deg = int(angle_deg % 360)
        dict_angle = cls.angle_dictionary_ready(part_name_list, part_name,
                                                angle_deg,
                                                cls.interprete(angle_deg))
        cordinate_node = {'x': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                          'y': angle_deg}
        cls.angles_chart_time_value[part_name_list + '_list'].append(cordinate_node)

        return dict_angle


    @classmethod
    def interprete(cls, angle):
        if angle > 40:
            return "perfect"
        if angle < 90:
            return "normal"


    @classmethod
    def angle_dictionary_ready(cls, part_name_list, part, angle, status):
        angle = {"part": part,
                 "part_name_list": part_name_list,
                 "angle": angle,
                 "status": status}
        return angle


    @classmethod
    def get_angle_data(cls):
        with cls.mp_pose.Pose(min_detection_confidence=.5, min_tracking_confidence=.5) as pose:
            while True:
                frame = cls.capture_image()
                results = pose.process(frame)
                if frame is not None:
                    yield cls.pose_landmarks(results)
                else:
                    break
                time.sleep(cls.timeframe)


    @classmethod
    def get_angle_data_chart_ready(cls):
        while True:

            frame = cls.capture_image()
            if cls.angles_chart_time_value is not None and frame is not None:
                yield cls.angles_chart_time_value
            else:
                break

    #
    # @classmethod
    # def get_angles_csv_ready(cls):
    #     with cls.mp_pose.Pose(min_detection_confidence=.5, min_tracking_confidence=.5) as pose:
    #         while True:
    #             frame = cls.capture_image()
    #             results = pose.process(frame)
    #             if frame is not None:
    #                 cls.csv_pose_landmarks(results)
    #                 yield cls.angles_csv
    #             else:
    #                 break
    #             time.sleep(cls.timeframe)


    @classmethod
    def make_excel(cls):
        time_index = []
        joints_list = {'left_knee': [],
                'left_elbow': [],
                'left_wrist': [],
                'left_shoulder': [],
                'right_knee': [],
                'right_elbow': [],
                'right_wrist': [],
                'right_shoulder': []}
        data = cls.angles_csv
        data_dict = {}
        for item in data:
            time_index.append(item['time'])

            for parts in item['angles']:
                joints_list[parts['part_name_list']].append(parts['angle'])
            # data_dict = {'time':item['time']}
            data_dict.setdefault('time', str(item['time']))

        df = pd.DataFrame(joints_list, index=time_index)
        df.to_excel(cls.output_folder+"/statics.xlsx")


    @classmethod
    def download_and_erase(cls):
        cls.make_excel()
        cls.release_camera()