import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn import tree
import joblib

result_df = pd.read_csv("C:/Users/serayyağcı/Desktop/heartProject/heartProjectApp/files/final_evaluation_data.csv")

def evaluate_model(model, x_test, y_test):
    # Predict Test Data
    y_pred = model.predict(x_test)

    # Calculate accuracy, precision, recall, f1-score, and kappa score
    acc = metrics.accuracy_score(y_test, y_pred)
    prec = metrics.precision_score(y_test, y_pred, pos_label="Yes")
    rec = metrics.recall_score(y_test, y_pred, pos_label="Yes")
    f1 = metrics.f1_score(y_test, y_pred, pos_label="Yes")
    kappa = metrics.cohen_kappa_score(y_test, y_pred)

    # Calculate area under curve (AUC)
    y_pred_proba = model.predict_proba(x_test)[::, 1]
    fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba, pos_label="Yes")
    auc = metrics.roc_auc_score(y_test, y_pred_proba)

    # Display confussion matrix
    cm = metrics.confusion_matrix(y_test, y_pred,labels =["Yes","No"])

    return {'acc': acc, 'prec': prec, 'rec': rec, 'f1': f1, 'kappa': kappa,
            'fpr': fpr, 'tpr': tpr, 'auc': auc, 'cm': cm, 'y_pred_prob':y_pred_proba}

#Independent Variable
X = result_df.drop('HeartDisease', axis= 1)

#Dependent Variables
y = result_df['HeartDisease']

#Split the data into the test and the train data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#Use the one hot encoding for the categorical data
X_train_encoded = pd.get_dummies(X_train)

X_test_encoded = pd.get_dummies(X_test)


# Scale the data
scaler_train = StandardScaler().fit(X_train_encoded)
X_train_encoded_scaled = scaler_train.transform(X_train_encoded)

# Save the scaler
joblib.dump(scaler_train, 'scaler_train.save')


# Scale test data
scaler_test = StandardScaler().fit(X_test_encoded)
X_test_encoded_scaled = scaler_test.transform(X_test_encoded)
# Save the scaler
joblib.dump(scaler_test, 'scaler_test.save')



# Train the model with Logistic Regression
clf_R = LogisticRegression(random_state=0)
clf_R.fit(X_train_encoded_scaled, y_train)
# Save the model
joblib.dump(clf_R, 'model_R.save')

# Train the model with Tree Classifier
clf_T = tree.DecisionTreeClassifier(random_state=0)
clf_T.fit(X_train_encoded_scaled, y_train)
# Save the model
joblib.dump(clf_T, 'model_T.save')




#Recall the model and the scaler required
model = joblib.load('model_R.save')
scaler = joblib.load('scaler_test.save')

# Predict the test data.
prediction = model.predict(X_test_encoded_scaled)

def input_taker(input_dict,column_list_num,column_list_bool):
    output_dict = dict()
    for i in column_list_num:
        if i in input_dict:
            output_dict[i] = input_dict[i]
    for j in column_list_bool:
        key,value = j.split("_",1)
        if input_dict[key][0] == value:
            output_dict[j] = True
        else:
            output_dict[j] = False
    data_frame = pd.DataFrame.from_dict(output_dict)
    return data_frame


def single_predictor(model,scaler,series):

    scaled_series = scaler.transform(series)
    prediction_categorical = model.predict(scaled_series)
    prediction_prob = model.predict_proba(scaled_series)
    return prediction_categorical,prediction_prob



column_list_numerical =['BMI', 'PhysicalHealth', 'MentalHealth', 'SleepTime']
column_list_boolean  = [ 'Smoking_No','Smoking_Yes', 'AlcoholDrinking_No', 'AlcoholDrinking_Yes', 'Stroke_No',
       'Stroke_Yes', 'DiffWalking_No', 'DiffWalking_Yes', 'Sex_Female',
       'Sex_Male', 'AgeCategory_18-24', 'AgeCategory_25-29',
       'AgeCategory_30-34', 'AgeCategory_35-39', 'AgeCategory_40-44',
       'AgeCategory_45-49', 'AgeCategory_50-54', 'AgeCategory_55-59',
       'AgeCategory_60-64', 'AgeCategory_65-69', 'AgeCategory_70-74',
       'AgeCategory_75-79', 'AgeCategory_80 or older',
       'Race_American Indian/Alaskan Native', 'Race_Asian', 'Race_Black',
       'Race_Hispanic', 'Race_Multiracial', 'Race_Other', 'Race_White',
       'Diabetic_No', 'Diabetic_Yes', 'PhysicalActivity_No',
       'PhysicalActivity_Yes', 'GenHealth_Excellent', 'GenHealth_Fair',
       'GenHealth_Good', 'GenHealth_Poor', 'GenHealth_Very good', 'Asthma_No',
       'Asthma_Yes', 'KidneyDisease_No', 'KidneyDisease_Yes', 'SkinCancer_No',
       'SkinCancer_Yes']


