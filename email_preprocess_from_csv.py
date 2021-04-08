import _pickle as cPickle
import numpy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif


def barplot(df, X, Y, figsize, color, orient, ylabel, xlabel, font_scale, rotation):
    f, ax = plt.subplots(figsize=figsize)
    sns.set_color_codes("muted")
    sns.barplot(x = X, y = Y, data = df, color = color, orient = orient)
    ax.set(ylabel = ylabel, xlabel = xlabel)
    sns.set(font_scale = font_scale)
    plt.xticks(rotation = rotation) 
    plt.show()



def preprocess_from_csv(csv_file = "C:\\Users\\preet\\workspace-neon\\Email-Classification-Supervised\\mail_list.csv"):
    """ 
        this function takes a pre-made csv of email data and performs
        a number of preprocessing steps:
            -- splits into training/testing sets (10% testing)
            -- vectorizes into tfidf matrix
            -- selects/keeps most helpful features

        after this, the feaures and labels are put into numpy arrays, which play nice with sklearn functions

        4 objects are returned:
            -- training/testing features
            -- training/testing labels

    """

    # read csv file
    data = pd.read_csv(csv_file)
    
    
    #print(data.isnull().sum())
    data.dropna(inplace = True)
    print("Rows with missing values have been removed")
    #print(data.isnull().sum())
    
    
    # Plot Bar to show how many emails from whom
    email_count = data["Category"].value_counts()
    indices = email_count.index
    count = pd.DataFrame(email_count, columns = ["Category"])
    count["Category names"] = indices
    barplot(df = count[:40], X = "Category", Y = "Category names", figsize = (7, 8), color = 'b', orient = 'h', ylabel = "Folders", xlabel = "Count", font_scale = 1.2, rotation = 90)
    
    
    # Pandas ".iloc" expects row_indexer, column_indexer  
    #X = data.iloc[:,:-1].values
    X = data['Body']
    # Now let's tell the dataframe which column we want for the target/labels.  
    y = data['Category']
    
    

    ### test_size is the percentage of events assigned to the test set
    ### (remainder go into training)
    features_train, features_test, labels_train, labels_test = train_test_split(X, y, test_size=0.1, random_state=42)
    

    ### text vectorization--go from strings to lists of numbers
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                 stop_words='english')
    features_train_transformed = vectorizer.fit_transform(features_train)
    features_test_transformed  = vectorizer.transform(features_test)
    

    ### feature selection, because text is super high dimensional and 
    ### can be really computationally chewy as a result
    selector = SelectPercentile(f_classif, percentile=10)
    selector.fit(features_train_transformed, labels_train)
    features_train_transformed = selector.transform(features_train_transformed).toarray()
    features_test_transformed  = selector.transform(features_test_transformed).toarray()
   
    ### info on the data
    #print("\nNo. of Chris training emails:", sum(labels_train))
    #print("\nNo. of Sara training emails:", len(labels_train)-sum(labels_train))
    
    return features_train_transformed, features_test_transformed, labels_train, labels_test
