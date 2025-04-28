// content.js

// Function to send the current URL to the Flask API for phishing detection
function checkPhishingUrl() {
    const currentUrl = window.location.href;  // Get the current page URL
  
    // Send the URL to the Flask API for prediction
    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: currentUrl }),  // Send the URL as JSON
    })
    .then(response => response.json())
    .then(data => {
      // Handle the response from the Flask API
      if (data.prediction === 'phishing') {
        alert('Warning: This URL is a potential phishing site!');
      } else {
        console.log('This URL seems safe.');
      }
    })
    .catch(error => {
      console.error('Error detecting phishing URL:', error);
    });
  }
  
  // Run the function to check the current URL when the content script is loaded
  checkPhishingUrl();
  