import sys
from time import time
import pickle
sys.path.append("C:\\Python\\Training\\ML\\Email classification\\")
#from email_preprocess import preprocess
from emailPreprocessorFromCSV import preprocess_from_csv
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test, vectorizer = preprocess_from_csv("data_labelled.csv")
print('Preprocessing complete')
print(features_train.shape)
print(labels_train.shape)
print(features_test.shape)
print(labels_test.shape)

# defining the classifier
clf = KNeighborsClassifier(n_neighbors=7, metric='euclidean')

#predicting the time of train and testing
t0 = time()
clf.fit(features_train, labels_train)
print("\nTraining time:", round(time()-t0, 3), "s\n")
t1 = time()
pred = clf.predict(features_test)
print("Predicting time:", round(time()-t1, 3), "s\n")

#calculating and printing the accuracy of the algorithm
print("Accuracy of KNN Algorithm: ", accuracy_score(pred,labels_test))

print("="*180)
print(accuracy_score(pred, labels_test))
print("="*180)
print(classification_report(pred, labels_test))
print("="*180)
print(confusion_matrix(pred, labels_test))
print("="*180)

#Saving model and vectorizer to file for reuse
with open('KNNModel_Vect.pkl', 'wb') as fout:
    pickle.dump((vectorizer, clf), fout)
print("Trained model saved to file")
