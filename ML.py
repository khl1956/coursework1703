import numpy as np
import math
import pandas as pd
from sklearn.linear_model import LogisticRegression
import csv

df = pd.read_csv('heart.csv')

x_matrix_prep = df.drop(columns=['target','cp', 'restecg','slope','ca','thal','fbs','exang','oldpeak',])
x_matrix_prep_show = df.drop(columns=['cp', 'restecg','slope','ca','thal','fbs','exang','oldpeak',])
# print(x_matrix_prep_show)
# print(x_matrix_prep)
# exit()

x_matrix = x_matrix_prep.to_numpy()

y_vector = df.target.to_numpy()

dev_x = [x_matrix[i] for i in range(0, len(x_matrix), 10)]
dev_y = [y_vector[i] for i in range(0, len(y_vector), 10)]

test_x = [x_matrix[2], x_matrix[297]]
test_y = [y_vector[2], y_vector[297]]


logistic = LogisticRegression(max_iter=10000)
logistic.fit(x_matrix, y_vector)

# print(x_matrix[297])
#
# print('Coefficient: \n', logistic.coef_)
# print('Intercept: \n', logistic.intercept_)
#
# print(x_matrix[2])

tr = 200

# print(logistic.predict([x_matrix[tr]]))
#
# print(logistic.predict_proba([x_matrix[tr]]))

prob = logistic.predict_proba([x_matrix[tr]])[0][1]

if prob < 0.35:
    print('Серьезной угрозы нет')
if prob >= 0.35 and prob < 0.7:
    print('Вам нужно обследоваться')
if prob >= 0.7:
    print('Срочно обратитесь к врачу!')

# print(x_matrix[tr])