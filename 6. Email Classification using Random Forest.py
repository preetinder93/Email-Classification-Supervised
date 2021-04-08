import sys
from time import time
sys.path.append("C:\\Users\\preet\\workspace-neon\\Email-Classification-Supervised\\")
from email_preprocess import preprocess
from email_preprocess_from_csv import preprocess_from_csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess_from_csv()

# defining the classifier
clf = RandomForestClassifier(max_depth=2, random_state=0)

#predicting the time of train and testing
t0 = time()
clf.fit(features_train, labels_train)
print("\nTraining time:", round(time()-t0, 3), "s\n")
t1 = time()
pred = clf.predict(features_test)
print("Predicting time:", round(time()-t1, 3), "s\n")

#calculating and printing the accuracy of the algorithm
print("Accuracy of Random Forest Algorithm: ", accuracy_score(pred,labels_test))

print("="*180)
print(accuracy_score(pred, labels_test))
print("="*180)
print(classification_report(pred, labels_test))
print("="*180)
print(confusion_matrix(pred, labels_test))
print("="*180)