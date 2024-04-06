import pickle
import cv2
from matplotlib import pyplot as plt
import mediapipe as mp
import numpy as np

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

predicted_character = ""
sentence = ""

# asl_image = cv2.imread('asl.jpg')

cap = cv2.VideoCapture(0)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks,  
                mp_hands.HAND_CONNECTIONS,  
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))
        while len(data_aux) < 84:
            data_aux.append(0)
        # while len(data_aux) < 42:
        #     data_aux.append(0)
        # data_aux = data_aux[:42]

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10

        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        cv2.putText(frame, predicted_character, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)

    
    # frame[10:210, 10:310] = asl_image 

    
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))

    cv2.imshow('frame', frame)
    key= cv2.waitKey(1)

    if key == ord('n'):
        if data_aux:
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]
            sentence += predicted_character
            print("Predicted sentence is:", sentence)
        else:
            sentence += " "
            print("Predicted sentence is:", sentence)

    else:
        if data_aux:
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]
        else:
            predicted_character = ""

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# from collections import Counter
# character_counts = Counter(sentence)
# plt.figure(figsize=(10, 6))
# plt.bar(character_counts.keys(), character_counts.values())
# plt.xlabel('Predicted Characters')
# plt.ylabel('Frequency')
# plt.title('Inference Results')
# plt.show()
