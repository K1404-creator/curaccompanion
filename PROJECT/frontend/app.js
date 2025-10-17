// -------------------- BACKEND URL DYNAMIC SELECTION --------------------
const BACKEND_URL =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000"
    : "https://curaccompanionbackend.onrender.com";
// -------------- SIMPLE PAGE NAVIGATION --------------
const navButtons = document.querySelectorAll('.nav-btn');
const pages = document.querySelectorAll('.page');

function showPage(pageId) {
  pages.forEach(p => p.classList.remove('active'));
  const el = document.getElementById(pageId);
  if (el) el.classList.add('active');

  navButtons.forEach(b => b.classList.remove('active'));
  const btn = Array.from(navButtons).find(x => x.dataset.target === pageId);
  if (btn) btn.classList.add('active');
}

document.addEventListener('DOMContentLoaded', () => {
  showPage('dashboard'); // show dashboard on startup
});

navButtons.forEach(b => {
  b.addEventListener('click', () => {
    const t = b.dataset.target;
    showPage(t);
  });
});

// -------------------- POST helper --------------------
async function postData(url = '', data = {}) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  return res.json();
}

function parseFormData(form){
  const obj = {};
  for (let [key, value] of new FormData(form).entries()){
    if (value === '') { obj[key] = value; continue; }
    obj[key] = value.includes('.') ? parseFloat(value) : parseInt(value);
    if (typeof obj[key] === 'number' && isNaN(obj[key])) obj[key] = parseFloat(value);
  }
  return obj;
}

// -------------------- Health score updater --------------------
async function sendAggEvent(feature, prediction){
  const payload = { user_id: "demo", feature, prediction };
  try {
    const agg = await postData(`${BACKEND_URL}/agg/event`, payload);
    if(agg && agg.health_score !== undefined){
      setHealthScore(agg.health_score);
    }
  } catch(e){
    console.error("Aggregator error", e);
  }
}

function setHealthScore(val){
  const el = document.getElementById('healthScore');
  if(!el) return;

  el.innerText = val;

  // Color coding
  if(val >= 80){
    el.style.color = "green";
  } else if(val >= 50){
    el.style.color = "orange";
  } else {
    el.style.color = "red";
  }
}

// -------------------- Generic handler --------------------
function handlePrediction(formId, resultId, url, spinnerId){
  const form = document.getElementById(formId);
  const resultDiv = document.getElementById(resultId);
  const spinner = document.getElementById(spinnerId);

  if(!form) return;

  form.addEventListener('submit', async e => {
    e.preventDefault();
    resultDiv.innerText = '';
    const data = parseFormData(form);

    if(spinner) spinner.classList.remove('hidden');
    try{
      const res = await postData(url, data);
      if(res && typeof res.Prediction !== 'undefined'){
        resultDiv.innerText = `Result: ${res.result} (Prediction: ${res.Prediction})`;
        sendAggEvent(formId.replace("Form",""), res.Prediction);
      } else if(res && typeof res.result !== 'undefined'){
        resultDiv.innerText = `Result: ${res.result}`;
      } else {
        resultDiv.innerText = 'No prediction returned.';
      }

      // history
      const hist = document.getElementById('history');
      if(hist){
        const time = new Date().toLocaleString();
        const line = document.createElement('div');
        line.style.marginTop = '8px';
        line.innerText = `${time} • ${formId} → ${resultDiv.innerText}`;
        if(hist.innerText.includes('No history')) hist.innerText = '';
        hist.prepend(line);
      }

    } catch(err){
      console.error(err);
      resultDiv.innerText = 'Error fetching prediction — check backend.';
    } finally{
      if(spinner) spinner.classList.add('hidden');
    }
  });
}

// -------------------- Connect forms --------------------
handlePrediction('diabetesForm','diabetesResult',`${BACKEND_URL}/diabetes/predict_diabetes`,'diabetesSpinner');
handlePrediction('heartForm','heartResult',`${BACKEND_URL}/heart/predict_heart`,'heartSpinner');
handlePrediction('neurotapForm','neurotapResult',`${BACKEND_URL}/neurotap/predict_neurotap`,'neurotapSpinner');

// -------------------- Chat page send logic --------------------
document.getElementById('sendChat')?.addEventListener('click', () => {
  const input = document.getElementById('chatInput');
  if (!input) return;
  const val = input.value.trim();
  if (!val) return;
  const area = document.getElementById('chatMessages');
  const el = document.createElement('div');
  el.style.textAlign = 'right';
  el.style.margin = '6px 0';
  el.innerHTML = `<div style="display:inline-block;background:#eef2ff;padding:8px;border-radius:8px">${val}</div>`;
  area.appendChild(el);
  input.value = '';

  const bot = document.createElement('div');
  bot.style.textAlign = 'left';
  bot.style.margin = '6px 0';
  bot.innerHTML = `<div style="display:inline-block;background:#f3f4f6;padding:8px;border-radius:8px">...</div>`;
  area.appendChild(bot);
  area.scrollTop = area.scrollHeight;

  fetch(`${BACKEND_URL}/chatbot/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: val })
  })
    .then(res => res.json())
    .then(data => {
      if (data && data.response) {
        bot.innerHTML = `<div style="display:inline-block;background:#f3f4f6;padding:8px;border-radius:8px">${data.response}</div>`;
      } else if (data && data.error) {
        bot.innerHTML = `<div style="display:inline-block;background:#f3f4f6;padding:8px;border-radius:8px;color:#dc2626">${data.error}</div>`;
      } else {
        bot.innerHTML = `<div style="display:inline-block;background:#f3f4f6;padding:8px;border-radius:8px">No response from bot.</div>`;
      }
      area.scrollTop = area.scrollHeight;
    })
    .catch(err => {
      bot.innerHTML = `<div style="display:inline-block;background:#f3f4f6;padding:8px;border-radius:8px;color:#dc2626">Error contacting bot.</div>`;
      area.scrollTop = area.scrollHeight;
    });
});
