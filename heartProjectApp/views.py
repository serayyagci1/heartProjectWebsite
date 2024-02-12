# yourappname/views.py
from django.shortcuts import render
from django.http import JsonResponse
import plotly.express as px
import logging

import json
from .models import Picture
from django.shortcuts import render
from .forms import HeartDiseaseForm
import joblib
from .files.new_data import evaluate_model, input_taker, single_predictor

column_list_numerical = ['BMI', 'PhysicalHealth', 'MentalHealth', 'SleepTime']
column_list_boolean = [ 'Smoking_No','Smoking_Yes', 'AlcoholDrinking_No', 'AlcoholDrinking_Yes', 'Stroke_No',
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

def choropleth_map(request):
    with open('heartProjectApp/files/merged.geojson') as geojson_file:
        geojson_data = json.load(geojson_file)

    # Convert 'HeartDiseasePercentage' values to floats
    for feature in geojson_data['features']:
        percentage_str = feature['properties'].get('HeartDiseasePercentage', None)
        try:
            percentage_float = float(percentage_str)
            feature['properties']['HeartDiseasePercentage'] = percentage_float
        except (TypeError, ValueError):
            feature['properties']['HeartDiseasePercentage'] = None

    locations = [feature['properties']['NAME'] for feature in geojson_data['features']]
    hover_names = [feature['properties']['NAME'] for feature in geojson_data['features']]
    color_values = [feature['properties']['HeartDiseasePercentage'] for feature in geojson_data['features']]

    fig = px.choropleth(
        geojson_data,
        geojson=geojson_data,
        locations=locations,
        featureidkey="properties.NAME",
        color=color_values,
        hover_name=hover_names,
        color_continuous_scale="reds",
    )

    fig.update_geos(fitbounds="locations", visible=False)
    # Set the initial zoom level
    fig.update_layout(
        autosize=False,
        margin = dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=4,
                autoexpand=True
            ),
            width=800,
    )

    graph = fig.to_html(full_html=False)

    return render(request, 'choropleth_map.html', {'graph': graph})
def home(request):
    choropleth_map_html = choropleth_map(request).content.decode("utf-8")
    images = Picture.objects.all()

    if request.method == 'POST':
        form = HeartDiseaseForm(request.POST, csv_columns=['BMI', 'Smoking', 'AlcoholDrinking', 'Stroke', 'PhysicalHealth', 'MentalHealth', 'DiffWalking', 'Sex', 'AgeCategory', 'Race', 'Diabetic', 'PhysicalActivity', 'GenHealth', 'SleepTime', 'Asthma', 'KidneyDisease', 'SkinCancer'])
        if form.is_valid():
            input_data = {
                'BMI': [float(form.cleaned_data['BMI'])],
                'PhysicalHealth': [float(form.cleaned_data['PhysicalHealth'])],
                'MentalHealth': [float(form.cleaned_data['MentalHealth'])],
                'SleepTime': [float(form.cleaned_data['SleepTime'])],
                'Smoking': [form.cleaned_data['Smoking']],
                'AlcoholDrinking': [form.cleaned_data['AlcoholDrinking']],
                'Stroke': [form.cleaned_data['Stroke']],
                'DiffWalking': [form.cleaned_data['DiffWalking']],
                'Sex': [form.cleaned_data['Sex']],
                'AgeCategory': [form.cleaned_data['AgeCategory']],
                'Race': [form.cleaned_data['Race']],
                'Diabetic': [form.cleaned_data['Diabetic']],
                'PhysicalActivity': [form.cleaned_data['PhysicalActivity']],
                'GenHealth': [form.cleaned_data['GenHealth']],
                'Asthma': [form.cleaned_data['Asthma']],
                'KidneyDisease': [form.cleaned_data['KidneyDisease']],
                'SkinCancer': [form.cleaned_data['SkinCancer']],
                # ... (other fields)
            }
            # Add logging to see the input_data
            logging.info(f"Input data: {input_data}")
            # Example usage of input_taker to prepare data for prediction
            input_series = input_taker(input_data, column_list_numerical, column_list_boolean)
            logging.info(f"Input series: {input_series}")
            # Load the saved model and scaler
            model_R = joblib.load('C:/Users/serayyağcı/Desktop/heartProject/heartProjectApp/files/model_R.save')
            scaler_test = joblib.load('C:/Users/serayyağcı/Desktop/heartProject/heartProjectApp/files/scaler_test.save')

            # Predict using Logistic Regression
            prediction_categorical, prediction_probability = single_predictor(model_R, scaler_test, input_series)
            print('Prediction categorical is: ' + str(prediction_categorical) + ' Prediction probability is: '+ str(prediction_probability))
            dict_2 = {"Yes": "Positive", "No": "Negative"}
            dict_3 = {"Yes": prediction_probability[0][1], "No": prediction_probability[0][0]}
            logistic_regression_results = f" Ml model predicts the Heart disease as {dict_2[prediction_categorical[0]]} with the probability of {dict_3[prediction_categorical[0]]} "

            # Return the result as JSON
            return JsonResponse({'logistic_regression_results': logistic_regression_results})
    else:
        form = HeartDiseaseForm()

    return render(request, 'home.html', {'form': form, 'images': images, 'choropleth_map': choropleth_map_html})


def display_images(request, category):
    images = Picture.objects.filter(category=category)
    return render(request, 'image_list.html', {'images': images})


