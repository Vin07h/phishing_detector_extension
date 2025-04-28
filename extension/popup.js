// popup.js

document.getElementById("checkBtn").addEventListener("click", function() {
    const url = document.getElementById("urlInput").value;
  
    // Check if the URL is empty
    if (url.trim() === "") {
      document.getElementById("result").textContent = "Please enter a URL.";
      return;
    }
  
    // Send the URL to the background script for checking
    chrome.runtime.sendMessage({ action: "checkPhishing", url: url }, function(response) {
      document.getElementById("result").textContent = response.message;
    });
  });
  