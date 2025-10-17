import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

data = pd.read_csv(r"C:\Users\Krish\Documents\PROJECT\dataset\diabetes.csv")

# print(data.head())

# print(data.describe()) # Statistical summary

# print(data.info()) # Check for missing values

# data.duplicated().sum() # Check for duplicates


# Data visualization


# plt.figure(figsize=(12, 6))

# sns.countplot(x='Outcome', data=data)  # 500 patients without diabetes and 268 with diabetes
# plt.show()


# #observing outliers

# plt.figure(figsize = (12,12))

# for i, col in enumerate(['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']):
#     plt.subplot(3,3,i+1)
#     sns.boxplot(x = col, data = data)

# plt.show()



# sns.pairplot(data, hue = 'Outcome', data = data)   # hue is used to specify the column for color coding
# plt.show()

# Standard scaling and label encoding


from sklearn.preprocessing import StandardScaler

sc_x = StandardScaler()
X = pd.DataFrame(sc_x.fit_transform(data.drop('Outcome', axis=1),), columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'])
y = data['Outcome']


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

from sklearn.neighbors import KNeighborsClassifier

test_score = []
train_score = []

for i in range(1,15):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    train_score.append(knn.score(X_train, y_train))
    test_score.append(knn.score(X_test, y_test))



max_train_score = max(train_score)
train_scores_index = [i for i, v in enumerate(train_score) if v == max_train_score]
print("Max Train Score {} % and k = {}".format(max_train_score*100,list(map(lambda x: x+1, train_scores_index))))



max_test_score = max(test_score)
test_scores_index = [i for i, v in enumerate(test_score) if v == max_test_score]
print("Max test Score {} % and k = {}".format(max_test_score*100,list(map(lambda x: x+1, test_scores_index))))



# creating model with k=13 as it is the best k value from above results


knn = KNeighborsClassifier(n_neighbors=13)
knn.fit(X_train, y_train)
print(knn.score(X_test, y_test) ) # model accuracy

from sklearn.metrics import classification_report, confusion_matrix

y_pred = knn.predict(X_test)
print(confusion_matrix(y_test, y_pred))




import joblib

joblib.dump(knn, 'models/diabetes_model.pkl')

joblib.dump(sc_x, 'models/scaler.pkl') # Save the scaler as well 