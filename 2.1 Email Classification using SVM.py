import sys
from time import time
sys.path.append("C:\\Users\\preet\\workspace-neon\\Email-Classification-Supervised\\")
from email_preprocess import preprocess
from email_preprocess_from_csv import preprocess_from_csv
from sklearn.svm import SVC
import pickle
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess_from_csv()

#defining the classifier
clf = SVC(kernel = 'linear', C=1)

#predicting the time of train and testing
t0 = time()
clf.fit(features_train, labels_train)
print("\nTraining time:", round(time()-t0, 3), "s\n")

"""
# save the model to disk
filename = 'finalized_model.sav'
pickle.dump(clf, open(filename, 'wb'))
"""

t1 = time()
pred = clf.predict(features_test)
print("Predicting time:", round(time()-t1, 3), "s\n")

"""
filename = 'finalized_model.sav'
# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
pred = loaded_model.predict(features_test)
"""

print("="*180)
print(accuracy_score(pred, labels_test))
print("="*180)
print(classification_report(pred, labels_test))
print("="*180)
print(confusion_matrix(pred, labels_test))
print("="*180)

