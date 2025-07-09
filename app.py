
from flask import Flask, request, render_template
import numpy as np
import joblib # Import joblib to load the model

app = Flask(__name__)

# Load the trained model
# Make sure 'logistic_regression_model.pkl' is in the same directory or provide the full path
try:
    model = joblib.load('logistic_regression_model.pkl')
except FileNotFoundError:
    model = None # Handle case where model file is not found
    print("Error: Model file 'logistic_regression_model.pkl' not found. Please train and save the model first.")
try:
    model = joblib.load('logistic_regression_model.pkl')
    print("✅ Model loaded successfully.")
except FileNotFoundError:
    model = None
    print("❌ Error: Model file 'logistic_regression_model.pkl' not found.")


# Define risk thresholds
LOW_RISK_THRESHOLD = 0.33
MEDIUM_RISK_THRESHOLD = 0.66


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    if model is None:
        prediction_text = "Error: Model not loaded. Please ensure 'logistic_regression_model.pkl' exists."
        return render_template('index.html', prediction_text=prediction_text)

    try:
        # Get input values from the form
        ap_hi = float(request.form['ap_hi'])
        ap_lo = float(request.form['ap_lo'])
        age = int(request.form['age'])
        cholesterol = int(request.form['cholesterol'])
        weight = float(request.form['weight'])

        # Create a numpy array from the input
        features = np.array([[ap_hi, ap_lo, age, cholesterol, weight]])

        # Predict probability using the trained model
        prediction_proba = model.predict_proba(features)[:, 1]
        risk_probability = prediction_proba[0]

        # Classify risk based on thresholds
        if risk_probability < LOW_RISK_THRESHOLD:
            risk_zone = "Low Risk"
        elif risk_probability < MEDIUM_RISK_THRESHOLD:
            risk_zone = "Medium Risk"
        else:
            risk_zone = "High Risk"

        prediction_text = f"Predicted CVD Risk Probability: {risk_probability:.4f} - Risk Zone: {risk_zone}"

    except Exception as e:
        prediction_text = f"Error: {e}"

    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    
    print("🚀 Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)

   



    # For running in a local environment
    # app.run(debug=True)

    # For running in Colab, you might use something like ngrok
    # See https://towardsdatascience.com/building-and-running-a-flask-app-in-google-colab-c02a571026c1
    pass
