import pandas as pd
import numpy as np

def call_ML_model():
  # reading the required files into python using pandas 
  df = pd.read_csv('self-healing script/train.csv')
  test = pd.read_csv('self-healing script/test.csv')
  # Fill the NaN values with 'None'
  df = df.fillna('None')
  # now since our machine learning model can only understand numeric values we'll have to convert the strings to numbers/indicator variables
  X_train = pd.get_dummies(df.drop('id',axis=1))
  # returns all the unique Elements stored in the training data
  df['id'].unique()
  # creating a dictionary of elements 
  element_dict = dict(zip(df['id'].unique(), range(df['id'].nunique())))
  # replacing dictionary values into dataframe as we meed to convert this into numbers
  y_train = df['id'].replace(element_dict)

  # Now we need to train our model , we can prefer any model which provides accurate results -
  # Random Forest Model
  from sklearn.ensemble import RandomForestClassifier
  rf = RandomForestClassifier(n_estimators=50, random_state=0)
  #print(len(X_train), len(y_train))
  rf.fit(X_train, y_train)

  # Calling the predict_elements method to return
  scores, element_name, test_df = predict_elements(test,rf,element_dict,df)
  #print(scores)
  print(element_name)
  # print(test_df)
  return element_name

def predict_elements(test,rf,element_dict,df):
    score = None
    num_of_records = len(test)
    test_ = test.fillna('None')
    concatenated = pd.concat([df, test_], axis=0).drop('id',axis=1)
    if num_of_records == 1:
        processed_test = pd.DataFrame(pd.get_dummies(concatenated).iloc[-(num_of_records)]).T
        probabilites = list(rf.predict_proba(processed_test.iloc[:,:])[0])
        element_name = list(element_dict.keys())[np.argmax(probabilites)]
        print ('Hence, the name of our predicted element is {}'.format(element_name))
        score = list(zip(df['id'].unique(), probabilites))

    elif num_of_records > 1:
        processed_test = pd.get_dummies(concatenated).iloc[-num_of_records:]
        probabilites = list(rf.predict_proba(processed_test))

        score = []
        for i in range(len(probabilites)):
            score.append(list(zip(df['id'].unique(), list(probabilites[i]))))

        element_index = np.argmax(probabilites, axis=1)
        element_name = []
        for ind_, i in enumerate(element_index):
            element_name.append(
                (ind_, 'Hence, the name of our predicted element is {}'.format(list(element_dict.keys())[i])))
    return score, element_name, test
