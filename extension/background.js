chrome.browserAction.onClicked.addListener(function(tab) {
  // This function will run when the extension icon is clicked
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const currentTab = tabs[0];
    const currentUrl = currentTab.url;

    // Send the current URL to the Flask API for phishing detection
    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: currentUrl }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.prediction === 'phishing') {
          alert('Warning: This URL is a phishing site!');
        } else {
          console.log('This URL seems safe.');
        }
      })
      .catch((error) => console.error('Error:', error));
  });
});
