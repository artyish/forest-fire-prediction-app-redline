import pandas as pd
from joblib import load
import webview

model = load('artifacts/model.joblib')
scaler = load('artifacts/scaler.joblib')

def preprocess_input(input_data):
    expected_columns = ['Temperature','windspeed','fuelmoisturecode','duffmoisturecode','initialspreadindex']
    df = pd.DataFrame(columns=expected_columns, index=[0])

    df['Temperature'] = input_data.get('Temperature', 0)
    df['windspeed'] = input_data.get('Windspeed', 0)
    df['fuelmoisturecode'] = input_data.get('Fuel Moisture Code', 0)
    df['duffmoisturecode'] = input_data.get('Duff Moisture Code', 0)
    df['initialspreadindex'] = input_data.get('Initial Spread Index', 0) 
    
    print("Preprocessing Input Data:")
    print(df)

    df = handlescaling(df)
    return df

def handlescaling(df):
    scaler_object = scaler
    columnstoscale = scaler_object['columnstoscale']
    scaleruse = scaler_object['scalertest']

    df[columnstoscale] = scaleruse.transform(df[columnstoscale])
    return df 

def predict(input_data):
    inputdf = preprocess_input(input_data)
    prediction = model.predict(inputdf)

    print("Prediction Probabilities:")
    print(prediction)

    return prediction

class Api:
    def handle_request(self, data):
        inputdata = {
            "Temperature": data['temperature'],
            "Wind Speed": data['windSpeed'],
            "Fuel Moisture Code": data['fuelmoisturecode'],
            "Duff Moisture Code": data['duffmoisturecode'],
            "Initial Spread Index": data['initialspreadindex']
        }

        print("Received input data:")
        print(inputdata)

        result = predict(inputdata)
        
        single_result = result[0]  
        print("Prediction Result:", single_result)
        
        return round(float(single_result * 100), 2)  

def start_webview():
    api = Api()
    window = webview.create_window('Forest Fire Prediction Model', 'index.html', width=1920, height=1080, js_api=api)
    webview.start()  

if __name__ == '__main__':
    start_webview()
