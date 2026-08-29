// DOM Elements
const chatApp = document.getElementById('chatApp'),
  sidebar = document.getElementById('sidebar'),
  menuToggleBtn = document.getElementById('menuToggleBtn'),
  toggleModeBtn = document.getElementById('toggleModeBtn'),
  closeBtn = document.getElementById('closeBtn'),
  toggleIcon = document.getElementById('toggleIcon'),
  toggleText = document.getElementById('toggleText'),
  clearBtn = document.getElementById('clearBtn'),
  newChatBtn = document.getElementById('newChatBtn'),
  resetViewBtn = document.getElementById('resetViewBtn'),
  chatTitle = document.getElementById('chatTitle'),
  emptyState = document.getElementById('emptyState'),
  messageList = document.getElementById('messageList'),
  chatScroll = document.getElementById('chatScroll'),
  composerForm = document.getElementById('composerForm'),
  draftInput = document.getElementById('draftInput'),
  sendBtn = document.getElementById('sendBtn'),
  recentList = document.getElementById('recentList'),
  quickGrid = document.getElementById('quickGrid');

// Data Collections (Tuned with Warm Amber & Earth Tones)
const quickActions = [
  { label: "Class timetable", prompt: "Show my class timetable for today", icon: "bi-calendar3", color: "#c88132,rgba(200,129,50,.14)" },
  { label: "Attendance", prompt: "What is my attendance status?", icon: "bi-clipboard-check", color: "#25855a,rgba(37,133,90,.14)" },
  { label: "Fee clearance", prompt: "Check my pending fees and receipts", icon: "bi-wallet2", color: "#3b8ea5,rgba(59,142,165,.14)" },
  { label: "Exam date sheet", prompt: "Show my upcoming exam dates", icon: "bi-file-earmark-text", color: "#8c5b30,rgba(140,91,48,.14)" }
];

const recentChats = [
  { title: "Fall 2026 Timetable", meta: "Today · 10:42 AM", prompt: "Show my class timetable for today" },
  { title: "Attendance Eligibility", meta: "Yesterday · 4:18 PM", prompt: "What is my attendance status?" },
  { title: "Semester Fee Receipt", meta: "Aug 26 · 11:05 AM", prompt: "Check my pending fees and receipts" }
];

let isThinking = false;

// 1. Render Recent Chats (Directly at top of sidebar)
function renderRecentChats() {
  recentList.innerHTML = '';
  recentChats.forEach(c => {
    const btn = document.createElement('button');
    btn.className = 'recent-chat';
    btn.innerHTML = `<i class="bi bi-chat-left-text"></i><span><strong>${c.title}</strong><small>${c.meta}</small></span>`;
    btn.onclick = () => {
      document.querySelectorAll('.recent-chat').forEach(x => x.classList.remove('active'));
      btn.classList.add('active');
      sendPrompt(c.prompt);
      sidebar.classList.remove('open');
    };
    recentList.appendChild(btn);
  });
}

// 2. Render Quick Suggestion Cards (2x2 Grid)
function renderQuickGrid() {
  quickGrid.innerHTML = '';
  quickActions.forEach(a => {
    const [fg, bg] = a.color.split(',');
    const btn = document.createElement('button');
    btn.className = 'quick-action';
    btn.innerHTML = `
      <span class="qicon" style="color:${fg};background:${bg}"><i class="bi ${a.icon}"></i></span>
      <span><strong>${a.label}</strong></span>
      <i class="bi bi-chevron-right ms-auto text-muted" style="font-size:11px"></i>
    `;
    btn.onclick = () => sendPrompt(a.prompt);
    quickGrid.appendChild(btn);
  });
}

// 3. Formatting & Responses
function formatTime() {
  return new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}

async function fetchResponse(prompt) {
  const token = localStorage.getItem('token');
  if (!token) {
    return "Error: You are not logged in. Please log in first.";
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ message: prompt })
    });

    if (!response.ok) {
      if (response.status === 401) {
        return "Your session has expired. Please log in again.";
      }
      return `Server error: ${response.statusText}`;
    }

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error("Chat API Error:", error);
    return "Sorry, I am unable to connect to the server right now.";
  }
}

// 4. Message Bubble Handlers
function addMessage(role, text) {
  const row = document.createElement('div');
  row.className = `msg-row ${role}`;
  row.innerHTML = `
    <div class="avatar ${role}">
      ${role === 'assistant' ? '<i class="bi bi-mortarboard-fill"></i>' : 'AM'}
    </div>
    <div class="msg-body">
      <div class="msg-meta">${role === 'assistant' ? 'UMS Assistant' : 'You'} · ${formatTime()}</div>
      <p>${text}</p>
    </div>
  `;
  messageList.appendChild(row);
  chatScroll.scrollTop = chatScroll.scrollHeight;
}

async function sendPrompt(raw) {
  const text = raw.trim();
  if (!text || isThinking) return;

  emptyState.style.display = 'none';
  messageList.style.display = 'flex';
  chatTitle.textContent = 'Academic support';

  addMessage('user', text);
  draftInput.value = '';
  sendBtn.disabled = true;
  isThinking = true;

  // Render thinking indicator
  const thinkRow = document.createElement('div');
  thinkRow.className = 'msg-row assistant';
  thinkRow.id = 'thinkingRow';
  thinkRow.innerHTML = `
    <div class="avatar assistant"><i class="bi bi-mortarboard-fill"></i></div>
    <div class="msg-body">
      <div class="msg-meta">UMS Assistant · thinking</div>
      <div class="thinking"><i></i><i></i><i></i></div>
    </div>
  `;
  messageList.appendChild(thinkRow);
  chatScroll.scrollTop = chatScroll.scrollHeight;

  const responseText = await fetchResponse(text);

  thinkRow.remove();
  addMessage('assistant', responseText);
  isThinking = false;
  sendBtn.disabled = !draftInput.value.trim();
  draftInput.focus();
}

// 5. Reset Conversation
function resetChat() {
  messageList.innerHTML = '';
  messageList.style.display = 'none';
  emptyState.style.display = 'block';
  chatTitle.textContent = 'Your academic command center';
  draftInput.value = '';
  sendBtn.disabled = true;
  sidebar.classList.remove('open');
  document.querySelectorAll('.recent-chat').forEach(x => x.classList.remove('active'));
}

// 6. Event Listeners
draftInput.addEventListener('input', () => {
  sendBtn.disabled = !draftInput.value.trim() || isThinking;
});

composerForm.addEventListener('submit', e => {
  e.preventDefault();
  sendPrompt(draftInput.value);
});

newChatBtn.addEventListener('click', resetChat);
clearBtn.addEventListener('click', resetChat);
resetViewBtn?.addEventListener('click', resetChat);

// Mobile Sidebar Toggle
menuToggleBtn?.addEventListener('click', () => {
  sidebar.classList.toggle('open');
});

// Close Assistant
closeBtn?.addEventListener('click', () => {
  window.location.href = '../dashboard_ui/index.html';
});

// Mode Switcher (Full-Screen ↔ Floating Widget)
toggleModeBtn.addEventListener('click', () => {
  const isFloating = chatApp.classList.toggle('mode-floating');
  chatApp.classList.toggle('mode-fullscreen', !isFloating);

  toggleIcon.className = isFloating ? 'bi bi-arrows-angle-expand' : 'bi bi-arrows-angle-contract';
  toggleText.textContent = isFloating ? 'Expand Window' : 'Float Window';

  if (!isFloating) {
    chatApp.style.transform = '';
    xOffset = 0;
    yOffset = 0;
  }

  setTimeout(() => {
    chatScroll.scrollTop = chatScroll.scrollHeight;
  }, 100);
});

// Keyboard Shortcut: Cmd/Ctrl + K for New Conversation
document.addEventListener('keydown', e => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    resetChat();
  }
});

// Initialize on Load
renderRecentChats();
renderQuickGrid();

// --- FLOATING WINDOW DRAG LOGIC ---
const topbar = document.querySelector('.topbar');
let isDragging = false;
let currentX;
let currentY;
let initialX;
let initialY;
let xOffset = 0;
let yOffset = 0;

topbar.addEventListener('mousedown', dragStart);
document.addEventListener('mouseup', dragEnd);
document.addEventListener('mousemove', drag);

function dragStart(e) {
  if (!chatApp.classList.contains('mode-floating')) return;
  // Ignore drag if clicking on a button inside the topbar
  if (e.target.closest('button')) return;

  initialX = e.clientX - xOffset;
  initialY = e.clientY - yOffset;

  isDragging = true;
  chatApp.classList.add('is-dragging');
}

function dragEnd(e) {
  initialX = currentX;
  initialY = currentY;
  isDragging = false;
  chatApp.classList.remove('is-dragging');
}

function drag(e) {
  if (isDragging) {
    e.preventDefault();
    currentX = e.clientX - initialX;
    currentY = e.clientY - initialY;

    xOffset = currentX;
    yOffset = currentY;

    chatApp.style.transform = `translate3d(${currentX}px, ${currentY}px, 0)`;
  }
}