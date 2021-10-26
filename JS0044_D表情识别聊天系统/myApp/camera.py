# import imutils
# import cv2
# import tensorflow as tf
# from keras.models import load_model
# from keras.preprocessing.image import img_to_array
# import numpy as np
# import sys
#
def openedCap():
    return "happey"
#     graph = tf.get_default_graph()
#
#     detection_model_path = './haarcascade_files/haarcascade_frontalface_default.xml'
#     emotion_model_path = './models/_mini_XCEPTION.102-0.66.hdf5'
#
#     # hyper-parameters for bounding boxes shape
#     # loading models
#     face_detection = cv2.CascadeClassifier(detection_model_path)
#     emotion_classifier = load_model(emotion_model_path, compile=False)
#     EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
#
#     emotion_classifier = load_model(emotion_model_path, compile=False)
#     cap = cv2.VideoCapture(0)
#     cap.set(3, 900)
#
#     cap.set(4, 900)
#     data=""
#     while(cap.isOpened()):
#         flag, frame = cap.read()
#
#         frame = imutils.resize(frame, width=300)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces =face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
#                                                 flags=cv2.CASCADE_SCALE_IMAGE)
#         canvas = np.zeros((250, 300, 3), dtype="uint8")
#         if len(faces) >0:
#             faces = sorted(faces, reverse=True,
#                            key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
#             (fX, fY, fW, fH) = faces
#             # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
#             # the ROI for classification via the CNN
#             roi = gray[fY:fY + fH, fX:fX + fW]
#             roi = cv2.resize(roi, (64, 64))
#             roi = roi.astype("float") / 255.0
#             roi = img_to_array(roi)
#             roi = np.expand_dims(roi, axis=0)
#             print("start……")
#             with graph.as_default():
#                 preds = emotion_classifier.predict(roi)[0]
#             print("End……")
#             emotion_probability = np.max(preds)
#             print(emotion_probability)
#             label = EMOTIONS[preds.argmax()]
#             print(label, type(label))
#             data=label
#
#             cv2.putText(frame, label, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 0), 2)
#             cv2.imshow('frame', frame)
#             if cv2.waitKey(3) & 0xFF == ord('q'):
#                 break
#     cap.release()
#     cv2.destroyAllWindows()
#     return data
# print("最终结果：",openedCap())
#
#
#
#
#
#
#
#
#
#
#
#
