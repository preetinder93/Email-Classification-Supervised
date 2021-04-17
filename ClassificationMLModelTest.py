import pickle
import pandas as pd
import sys
from time import time
from email_preprocess_from_csv import preprocess_from_csv


    

modelFile = "KNNModel_Vect.pkl"

with open(modelFile, 'rb') as f:
    vect, model = pickle.load(f)

def predictClass(text):
    return model.predict(vect.transform(text))

data = pd.read_csv('test_data.csv')
data.dropna(inplace = True)
print("Rows with missing values have been removed")

print(data.head(30))
print('\n **********************************************')

X_test = data['Body']
y_test = data['Category']

##print('Reached Here')
##KNN_prediction = model.predict(vect.transform(X_test))

for x in X_test:
    print(predictClass([x]))
    print('='*70)




#print(accuracy_score(KNN_prediction, y_test))
