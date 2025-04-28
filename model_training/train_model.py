import pandas as pd
import numpy as np
import scipy.sparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib

# Load your data
df = pd.read_csv('datasets\\urldata.csv')

# Feature engineering (you can modify this based on your dataset)
df['url_length'] = df['url'].apply(len)
df['num_subdomains'] = df['url'].apply(lambda x: x.count('.'))
df['num_special_chars'] = df['url'].apply(lambda x: sum(1 for char in x if not char.isalnum()))

# Split the data into features (X) and labels (y)
X = df[['url', 'url_length', 'num_subdomains', 'num_special_chars']]  # Including the new features
y = df['label']  # Assuming your label column is named 'label'

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorization for 'url' feature (this will create a sparse matrix)
vectorizer = TfidfVectorizer(stop_words='english')
X_train_vect = vectorizer.fit_transform(X_train['url'])
X_test_vect = vectorizer.transform(X_test['url'])

# Process additional features and convert them into a sparse matrix (to save memory)
additional_features_train = X_train[['url_length', 'num_subdomains', 'num_special_chars']].values
additional_features_test = X_test[['url_length', 'num_subdomains', 'num_special_chars']].values

# Convert the additional features to sparse format
additional_features_train_sparse = scipy.sparse.csr_matrix(additional_features_train)
additional_features_test_sparse = scipy.sparse.csr_matrix(additional_features_test)

# Combine the TF-IDF features with the additional features (sparse format)
X_train_final = scipy.sparse.hstack((X_train_vect, additional_features_train_sparse))
X_test_final = scipy.sparse.hstack((X_test_vect, additional_features_test_sparse))

# Initialize the Naive Bayes model
model = MultinomialNB()

# Train the model
model.fit(X_train_final, y_train)

# Predict on the test data
y_pred = model.predict(X_test_final)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Save the model and the vectorizer
joblib.dump(model, 'phishing_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

print("Model and vectorizer saved successfully.")
