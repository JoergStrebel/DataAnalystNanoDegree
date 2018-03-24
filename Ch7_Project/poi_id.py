#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import seaborn as sn

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# reused from https://discussions.udacity.com/t/pickling-pandas-df/174753/2
df = pd.DataFrame.from_records(list(data_dict.values()))
employees = pd.Series(list(data_dict.keys()))
df.set_index(employees, inplace=True)

# You will have code here to add columns, i.e. new features,
# to the df, or remove rows, i.e. employees, from the df
df.replace(to_replace='NaN', value=numpy.nan, inplace=True)

#Export for manual inspection
df.to_csv('./my_pandas_dataset.csv')

#count NA per column
print df.isnull().sum(axis=0).sort_values()

# drop column email_address, as it is a non-numeric feature and not informative
# drop columns with high NaN count
for col in ['email_address', 'deferral_payments', 'restricted_stock_deferred', 
        'director_fees', 'loan_advances']: 
    df.pop(col)

# Replace NA with 0 for calculations
df = df.fillna(0)

print df.describe()

### Task 2: Remove outliers
df.drop('TOTAL', axis=0, inplace=True)
# this does not sound like a real person
df.drop('THE TRAVEL AGENCY IN THE PARK', axis=0, inplace=True) 

### Task 3: Create new feature(s)
# https://discussions.udacity.com/t/getting-started-with-ml-project/342397/9
df['bonus_to_salary_ratio'] = df.bonus.div(df.salary, axis=0).fillna(0)
df['lti_ratio'] = df['long_term_incentive'].div(df['total_payments'], 
                                                axis=0).fillna(0)
df['shared_ratio'] = df['shared_receipt_with_poi'].div(df['to_messages'], 
                                                axis=0).fillna(0)

# visualize features by PoI status
# https://discussions.udacity.com/t/eda-on-financial-features/192556/19
#===============================================================================
for ind in df:
    if ind != 'poi':
        uquantile = df[ind].quantile(0.999)
        dquantile = df[ind].quantile(0.001)
        # get rid of outliers
        ax = df[(df[ind]<uquantile) & (df[ind]>dquantile)].boxplot(column=ind, 
                                                                   by = 'poi')                        
        plt.legend()        
        ax.set_ylim(dquantile, uquantile)
        plt.show()               

        

# after you create features, the column names will be your new features
# create a list of column names:
new_features_list = list(df.columns.values)
# remove 'poi' from the list
new_features_list.remove('poi')
# then add 'poi' as the first item (i.e. 0 position) in the list
new_features_list.insert(0, "poi")

# create a dictionary from the dataframe
my_dataset = df.to_dict('index')

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, new_features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit

# Boundaries for feature selection tuning
CONST_LOW_FEAT_NR = 4
CONST_HIGH_FEAT_NR = 14

# Automatic feature selection and validation for GaussianNB
# Establish a pipeline
# based on https://discussions.udacity.com/t/error-using-pipeline/171750/6

# Validation strategy
cv_sss = StratifiedShuffleSplit(n_splits=100, test_size = 0.3, random_state = 42)
oSKB=SelectKBest(score_func=f_classif)

# Algorithm selection
strAlgo = 'DecisionTreeClassifier'
         
if strAlgo=='GaussianNB':
    base_clf = GaussianNB()
    
    pipe = Pipeline(steps=[('feature_selection', oSKB),("clf", base_clf)])
    parameters ={"feature_selection__k": range(CONST_LOW_FEAT_NR, 
                                               CONST_HIGH_FEAT_NR)}
    
    grid_search = GridSearchCV(pipe, parameters, n_jobs = -1, cv = cv_sss, 
                               scoring = 'f1')        
    grid_search.fit(features, labels)
    

if strAlgo=='DecisionTreeClassifier':
    base_clf = DecisionTreeClassifier()       
    #https://discussions.udacity.com/t/eda-on-financial-features/192556/46    
    
    pipe = Pipeline(steps=[('feature_selection', oSKB),("clf", base_clf)])        
              
    parameters = {"feature_selection__k": range(CONST_LOW_FEAT_NR, 
                                                CONST_HIGH_FEAT_NR), 
             'clf__min_samples_split' : [5,6,7],
              'clf__min_samples_leaf' : [2,3,4],
              'clf__random_state' : [42],
              'clf__presort' : [True],
              'clf__class_weight' : [{0:1, 1:2}, {0:1, 1:1}]}
    grid_search = GridSearchCV(pipe, parameters, scoring = 'f1', 
                               n_jobs=-1, verbose=1, cv = cv_sss)
    grid_search.fit(features,labels)


OptKBS = grid_search.best_estimator_.named_steps['feature_selection']
# Retrieve the features 
KBest_features_list=[new_features_list[i+1] for i in 
                      OptKBS.get_support(indices=True)]
print()
print("Selected features:")
print KBest_features_list
 
# Get SelectKBest scores, rounded to 2 decimal places, 
feature_scores = ['%.2f' % elem for elem in OptKBS.scores_ ]
# Get SelectKBest pvalues, rounded to 3 decimal places, 
feature_scores_pvalues = ['%.3f' % elem for elem in OptKBS.pvalues_ ]
    # create a tuple of feature names, scores and pvalues, 
features_selected_tuple=[(new_features_list[i+1], feature_scores[i], 
                           feature_scores_pvalues[i]) for i in 
                           OptKBS.get_support(indices=True)]

# Sort the tuple by score, in reverse order
features_selected_tuple = sorted(features_selected_tuple, 
                                key=lambda feature: float(feature[1]) , 
                                reverse=True)

print ' '
print 'Selected Features, Scores, P-Values'
print features_selected_tuple

# Feature importances
if strAlgo=='DecisionTreeClassifier':
    best_dt = grid_search.best_estimator_.named_steps['clf']
    feature_importances = ['%.2f' % elem for elem in best_dt.feature_importances_ ]
    # create a tuple of feature names, scores and pvalues,    
    features_importance_tuple=[(KBest_features_list[i], feature_importances[i]) 
                               for i in range(len(feature_importances))]

    # Sort the tuple by score, in reverse order
    features_importance_tuple = sorted(features_importance_tuple, 
                                key=lambda feature: float(feature[1]) , 
                                reverse=True)    
    print ' '
    print 'Features Importances, Scores'
    print "Number of features: ", best_dt.n_features_
    print features_importance_tuple    

# make sure, there is poi as first feature.
KBest_features_list.insert(0, "poi")
        
# Evaluation
print()
print("Detailed classification report:")
test_classifier(grid_search.best_estimator_, my_dataset, KBest_features_list)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(grid_search.best_estimator_, my_dataset, 
                         KBest_features_list)


