import sys
from time import time
sys.path.append("C:\\Users\\preet\\workspace-neon\\Email-Classification-Supervised\\")
from email_preprocess import preprocess
from email_preprocess_from_csv import preprocess_from_csv
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess_from_csv()


#the code in this py file is more or less similar to the one in 2.1. Email classification using SVM
#however, this code has been altered and to train it on a smaller training dataset
#the tradeoff is that the accuracy almost always goes down when you do this
features_train = features_train[:len(features_train)//100]
labels_train = labels_train[:len(labels_train)//100]
#these lines effectively slice the training dataset down to 1% of its original size
#tossing out 99% of the training data. You can leave all other code unchanged.

#defining the classifier
clf = SVC()

#predicting the time of train and testing
t0 = time()
clf.fit(features_train, labels_train)
print("\nTraining time:", round(time()-t0, 3), "s\n")
t1 = time()
pred = clf.predict(features_test)
print("Predicting time:", round(time()-t1, 3), "s\n")

#calculating and printing the accuracy of the algorithm
print("Accuracy of SVM Algorithm with 1% Training Data: ", clf.score(features_test, labels_test))

print("="*180)
print(accuracy_score(pred, labels_test))
print("="*180)
print(classification_report(pred, labels_test))
print("="*180)
print(confusion_matrix(pred, labels_test))
print("="*180)