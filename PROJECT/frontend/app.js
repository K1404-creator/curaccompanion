// Helper function to POST data
async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    return response.json();
}

// Convert form values to correct type (int or float)
function parseFormData(form) {
    const obj = {};
    for (let [key, value] of new FormData(form).entries()) {
        // Check if the value contains a decimal → float, otherwise int
        obj[key] = value.includes('.') ? parseFloat(value) : parseInt(value);
    }
    return obj;
}

// Diabetes Prediction
document.getElementById('diabetesForm').addEventListener('submit', async e => {
    e.preventDefault();
    const formData = parseFormData(e.target);
    const result = await postData('http://127.0.0.1:8000/diabetes/predict_diabetes', formData);
    document.getElementById('diabetesResult').innerText = `Result: ${result.result} (Prediction: ${result.Prediction})`;
});

// Heart Disease Prediction
document.getElementById('heartForm').addEventListener('submit', async e => {
    e.preventDefault();
    const formData = parseFormData(e.target);
    const result = await postData('http://127.0.0.1:8000/heart/predict_heart', formData);
    document.getElementById('heartResult').innerText = `Result: ${result.result} (Prediction: ${result.Prediction})`;
});

// NeuroTaps Fatigue Detection
document.getElementById('neurotapForm').addEventListener('submit', async e => {
    e.preventDefault();
    const formData = parseFormData(e.target);
    const result = await postData('http://127.0.0.1:8000/neurotap/predict_neurotap', formData);
    document.getElementById('neurotapResult').innerText = `Result: ${result.result} (Prediction: ${result.Prediction})`;
});