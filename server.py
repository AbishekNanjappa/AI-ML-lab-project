import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

app = Flask(__name__)
CORS(app) 
# ...

# Load the dataset
df = pd.read_csv("cardio_train.csv", sep=";")
data = pd.read_csv("cardio_train.csv", sep=";")
df.drop(df[(df['height'] > df['height'].quantile(0.975)) | (df['height'] < df['height'].quantile(0.025))].index, inplace=True)
df.drop(df[(df['weight'] > df['weight'].quantile(0.975)) | (df['weight'] < df['weight'].quantile(0.025))].index, inplace=True)
df.drop(df[(df['ap_hi'] > df['ap_hi'].quantile(0.975)) | (df['ap_hi'] < df['ap_hi'].quantile(0.025))].index, inplace=True)
df.drop(df[(df['ap_lo'] > df['ap_lo'].quantile(0.975)) | (df['ap_lo'] < df['ap_lo'].quantile(0.025))].index, inplace=True)
data.drop("id", axis=1, inplace=True)
data.drop_duplicates(inplace=True)
data["bmi"] = data["weight"] / (data["height"]/100)**2
out_filter = ((data["ap_hi"] > 250) | (data["ap_lo"] > 200))
data = data[~out_filter]
out_filter3 = ((data["bmi"] > 43))
data = data[~out_filter3]
out_filter2 = ((data["ap_hi"] < 0) | (data["ap_lo"] < 0))
data = data[~out_filter2]
target_name = 'cardio'
data_target = data[target_name]
data = data.drop([target_name], axis=1)
train, test, target, target_test = train_test_split(data, data_target, test_size=0.1, random_state=0)
gbc = GradientBoostingClassifier()
gbc.fit(train, target)

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve input data from the request
    input_data = request.get_json()
    
    # Extract input values from the data
    age = input_data['age'] * 365.25
    gender = input_data['gender']
    height = input_data['height']
    weight = input_data['weight']
    ap_hi = input_data['ap_hi']
    ap_lo = input_data['ap_lo']
    cholesterol = input_data['cholesterol']
    gluc = input_data['gluc']
    smoke = input_data['smoke']
    alco = input_data['alco']
    active = input_data['active']
    bmi = weight / (height / 100) ** 2
    
    # Create input data object
    input_data = pd.DataFrame({
        'age': [age],
        'gender': [gender],
        'height': [height],
        'weight': [weight],
        'ap_hi': [ap_hi],
        'ap_lo': [ap_lo],
        'cholesterol': [cholesterol],
        'gluc': [gluc],
        'smoke': [smoke],
        'alco': [alco],
        'active': [active],
        'bmi': [bmi]
    })

    # Perform prediction
    prediction = gbc.predict(input_data)
    
    # Prepare the prediction result
    result = {
        'prediction': int(prediction[0])
    }
    
    # Return the prediction result as JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001)
