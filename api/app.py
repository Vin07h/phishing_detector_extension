from flask import Flask, request, jsonify
import joblib
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Configure the Flask-Limiter for rate limiting
limiter = Limiter(get_remote_address)  # Correct initialization

# Set up logging (log requests and errors)
log_file ='logs\\phishing_api.log'

# Check if logs directory exists, if not, create it
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load pre-trained model and vectorizer
model = joblib.load(r'api\phishing_model.pkl')
vectorizer = joblib.load(r'api\vectorizer.pkl')

@app.route('/predict', methods=['POST'])
@limiter.limit("10 per minute")  # Limit to 10 requests per minute per IP
def predict():
    try:
        # Get URL from the POST request
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'No URL provided!'}), 400

        # Log the incoming URL for auditing purposes
        logging.info(f"Received URL for prediction: {url}")

        # Transform the URL using the pre-trained vectorizer
        url_vector = vectorizer.transform([url])

        # Predict using the loaded model
        prediction = model.predict(url_vector)

        # Convert prediction (0 = Safe, 1 = Phishing) to string
        result = 'Phishing' if prediction[0] == 1 else 'Safe'

        # Log the prediction result
        logging.info(f"Prediction result for URL: {url} is {result}")

        # Return the result as a JSON response
        return jsonify({'prediction': result})

    except Exception as e:
        # Log the error
        logging.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
