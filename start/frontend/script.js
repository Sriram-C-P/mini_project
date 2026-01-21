function scanURL() {
    const url = document.getElementById("urlInput").value;
    const resultBox = document.getElementById("resultBox");
    const resultText = document.getElementById("resultText");
    const confidenceText = document.getElementById("confidenceText");

    if (!url) {
        alert("Please enter a URL");
        return;
    }

    // TEMP MOCK LOGIC (replace with backend API later)
    const isPhishing = url.includes("login") || url.includes("secure");

    resultBox.classList.remove("hidden", "safe", "phishing");

    if (isPhishing) {
        resultBox.classList.add("phishing");
        resultText.innerText = "⚠️ PHISHING DETECTED";
        confidenceText.innerText = "Confidence: 87%";
    } else {
        resultBox.classList.add("safe");
        resultText.innerText = "✅ LEGITIMATE WEBSITE";
        confidenceText.innerText = "Confidence: 92%";
    }
}
