// ---------- Date helpers ----------
const today = new Date();

function dayOfYear(d) {
  const start = new Date(d.getFullYear(), 0, 0);
  const diff = d - start;
  return Math.floor(diff / 86400000);
}

document.getElementById('today-date').textContent = today.toLocaleDateString(undefined, {
  weekday: 'long', month: 'long', day: 'numeric'
});

// ---------- Tab navigation ----------
const tabButtons = document.querySelectorAll('.tab-btn');
const views = document.querySelectorAll('.view');

tabButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    tabButtons.forEach(b => b.classList.remove('active'));
    views.forEach(v => v.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('view-' + btn.dataset.view).classList.add('active');
  });
});

// ---------- Prayers ----------
const prayersList = document.getElementById('prayers-list');

// Morning Offering is featured front-and-center
const morningOffering = PRAYERS.find(p => p.id === 'morning-offering');
if (morningOffering) {
  const featured = document.createElement('div');
  featured.className = 'card featured';
  featured.innerHTML = `<h2>${morningOffering.title}</h2><p class="body">${morningOffering.text}</p>`;
  prayersList.appendChild(featured);
}

// Group remaining prayers by category, in accordions
const groups = {};
PRAYERS.filter(p => p.id !== 'morning-offering').forEach(p => {
  (groups[p.group] = groups[p.group] || []).push(p);
});

Object.keys(groups).forEach(groupName => {
  const label = document.createElement('div');
  label.className = 'group-label';
  label.textContent = groupName;
  prayersList.appendChild(label);

  groups[groupName].forEach(prayer => {
    const item = document.createElement('div');
    item.className = 'accordion-item';
    item.innerHTML = `
      <button class="accordion-header">
        <span>${prayer.title}</span>
        <span class="chev">▾</span>
      </button>
      <div class="accordion-body">
        <div class="inner">${prayer.text}</div>
      </div>
    `;
    const header = item.querySelector('.accordion-header');
    const body = item.querySelector('.accordion-body');
    header.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      if (isOpen) {
        body.style.maxHeight = null;
        item.classList.remove('open');
      } else {
        item.classList.add('open');
        body.style.maxHeight = body.scrollHeight + 'px';
      }
    });
    prayersList.appendChild(item);
  });
});

// ---------- Readings ----------
function uscccbReadingsUrl(d) {
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  const yy = String(d.getFullYear()).slice(-2);
  return `https://bible.usccb.org/bible/readings/${mm}${dd}${yy}.cfm`;
}
document.getElementById('readings-link').href = uscccbReadingsUrl(today);

// ---------- Finance ----------
const financeTitle = document.getElementById('finance-title');
const financeBody = document.getElementById('finance-body');
const financeTopics = document.getElementById('finance-topics');
const financeDoneCheck = document.getElementById('finance-done-check');
const financeDoneLabel = document.getElementById('finance-done-label');
const financeDoneRow = document.getElementById('finance-done-row');

let currentFinanceArticle = FINANCE_ARTICLES[dayOfYear(today) % FINANCE_ARTICLES.length];

function showFinanceArticle(article) {
  currentFinanceArticle = article;
  financeTitle.textContent = article.title;
  financeBody.textContent = article.body;

  // Highlight active topic in the list
  financeTopics.querySelectorAll('button').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.id === article.id);
  });

  refreshDoneState();
}

function readKey(article) {
  return 'finance-read-' + article.id + '-' + today.toISOString().slice(0, 10);
}

function refreshDoneState() {
  const done = localStorage.getItem(readKey(currentFinanceArticle)) === '1';
  financeDoneCheck.checked = done;
  financeDoneRow.classList.toggle('done', done);
  financeDoneLabel.textContent = done ? 'Read today ✓' : 'Mark as read';
}

financeDoneCheck.addEventListener('change', () => {
  const key = readKey(currentFinanceArticle);
  if (financeDoneCheck.checked) {
    localStorage.setItem(key, '1');
  } else {
    localStorage.removeItem(key);
  }
  refreshDoneState();
});

FINANCE_ARTICLES.forEach(article => {
  const btn = document.createElement('button');
  btn.textContent = article.title;
  btn.dataset.id = article.id;
  btn.addEventListener('click', () => showFinanceArticle(article));
  financeTopics.appendChild(btn);
});

showFinanceArticle(currentFinanceArticle);

// ---------- Service worker (offline support) ----------
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  });
}
