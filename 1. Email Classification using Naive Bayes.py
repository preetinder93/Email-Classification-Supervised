import sys
from time import time
sys.path.append("C:\\Users\\preet\\workspace-neon\\Email-Classification-Supervised\\")
from email_preprocess import preprocess
from email_preprocess_from_csv import preprocess_from_csv
import numpy as np

#using the Gaussian Bayes algorithm for classification of emails.
#the algorithm is imported from the sklearn library
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

#initializaing the test and train features and labels
#the function preprocess is imported from email_preprocess.py 
features_train, features_test, labels_train, labels_test = preprocess_from_csv()

#defining the classifier
clf = GaussianNB()

#predicting the time of train and testing
t0 = time()
clf.fit(features_train, labels_train)
print("\nTraining time:", round(time()-t0, 3), "s\n")
t1 = time()
pred = clf.predict(features_test)
print("Predicting time:", round(time()-t1, 3), "s\n")

#calculating and printing the accuracy
print("Accuracy of Naive Bayes: ", accuracy_score(pred,labels_test))

print("="*180)
print(accuracy_score(pred, labels_test))
print("="*180)
print(classification_report(pred, labels_test))
print("="*180)
print(confusion_matrix(pred, labels_test))
print("="*180)



