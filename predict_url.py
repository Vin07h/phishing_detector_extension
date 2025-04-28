import joblib

# Load the trained model and vectorizer
model = joblib.load('phishing_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Take URL input from user
new_url = input("Enter a URL to check: ")
# Transform the URL using the loaded vectorizer
url_vector = vectorizer.transform([new_url])

# Predict using the loaded model
prediction = model.predict(url_vector)

# Display the result
if prediction[0] == 1:
    print("⚠️  This URL is likely PHISHING!")
else:
    print("✅  This URL seems SAFE!")
