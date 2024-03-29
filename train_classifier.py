import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

try:
    data_dict = pickle.load(open('./data.pickle', 'rb'))
    data = data_dict['data']
    labels = data_dict['labels']

    # Find the maximum length of arrays in the data
    max_length = max(len(item) for item in data)

    # Pad arrays in data to make them all the same length
    data = [item + [0] * (max_length - len(item)) for item in data]

    data = np.asarray(data)
    labels = np.asarray(labels)

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

    model = RandomForestClassifier()
    
    model.fit(x_train, y_train)

    y_predict = model.predict(x_test)

    score = accuracy_score(y_predict, y_test)

    print('{}% of samples were classified correctly!'.format(score * 100))

    with open('model.p', 'wb') as f:
        pickle.dump({'model': model}, f)
except Exception as e:
    print("An error occurred:", e)
