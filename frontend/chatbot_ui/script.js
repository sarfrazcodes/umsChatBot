// DOM Elements
const chatApp = document.getElementById('full-page'),
  closeBtn = document.getElementById('closeBtn'),
  toggleModeBtn = document.getElementById('toggle-float-btn'),
  toggleIcon = toggleModeBtn.querySelector('i'),
  newChatBtn = document.getElementById('newChatBtn'),
  emptyState = document.getElementById('empty-state'),
  messagesEl = document.getElementById('messages'),
  textarea = document.getElementById('chat-textarea'),
  sendBtn = document.getElementById('send-btn'),
  recentList = document.getElementById('chat-history'),
  quickGrid = document.getElementById('quick-prompts');

// Data Collections
const chatHistoryData = [
  {icon:"fa-regular fa-clock",title:"Attendance requirem...",when:"Today"},
  {icon:"fa-regular fa-circle-question",title:"Find a campus service",when:"Yesterday"},
  {icon:"fa-regular fa-file-lines",title:"Semester exam dates",when:"28 Aug"},
];
const quickPromptsData = [
  {icon:"fa-regular fa-clock",label:"Attendance",q:"How is my attendance?"},
  {icon:"fa-regular fa-calendar",label:"Timetable",q:"Show my next class"},
  {icon:"fa-regular fa-file-lines",label:"Exams",q:"When are my exams?"},
  {icon:"fa-regular fa-envelope",label:"Fees",q:"Check my fee status"},
];

let isThinking = false;

// 1. Render Recent Chats
function renderRecentChats() {
  recentList.innerHTML = chatHistoryData.map(h=>`
    <button class="hist-item d-flex align-items-center gap-2">
      <span class="hist-icon"><i class="${h.icon}"></i></span>
      <span class="flex-grow-1 text-start"><div class="fw-semibold small">${h.title}</div><div class="text-muted-sm">${h.when}</div></span>
      <i class="fa-solid fa-chevron-right text-muted small"></i>
    </button>`).join("");
}

// 2. Render Quick Prompts
function renderQuickPrompts() {
  quickGrid.innerHTML = quickPromptsData.map(p=>`
    <button class="prompt-card d-flex align-items-center gap-2">
      <span class="hist-icon"><i class="${p.icon}"></i></span>
      <span class="flex-grow-1 text-start"><div class="text-muted-sm">${p.label}</div><div class="fw-semibold small">${p.q}</div></span>
      <i class="fa-solid fa-chevron-right text-muted small"></i>
    </button>`).join("");
}

// Clicking a quick prompt sends it straight away
quickGrid.addEventListener("click", e=>{
  const card = e.target.closest(".prompt-card");
  if(!card) return;
  sendMessage(card.querySelector(".fw-semibold").textContent);
});

// 3. Chat Logic
function escapeHtml(str){
  return str.replace(/[&<>"']/g, m => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
}

function addMessage(text, from){
  const row = document.createElement("div");
  row.className = `msg-row ${from}`;
  
  let formattedText = escapeHtml(text);
  // Optional: convert **bold** to <strong>bold</strong>
  formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  formattedText = formattedText.replace(/\n/g, '<br>');
  
  row.innerHTML = `<div class="msg">${formattedText}</div>`;
  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return row;
}

// Typing Effect Function for Bot Responses
async function addTypingMessage(text, from) {
  return new Promise(resolve => {
    const row = document.createElement("div");
    row.className = `msg-row ${from}`;
    const msgBubble = document.createElement("div");
    msgBubble.className = "msg";
    row.appendChild(msgBubble);
    messagesEl.appendChild(row);
    
    let formattedText = escapeHtml(text);
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedText = formattedText.replace(/\n/g, '<br>');
    
    let i = 0;
    function typeWriter() {
      if (i < formattedText.length) {
        // Handle HTML Tags so we don't print them letter-by-letter
        if (formattedText.charAt(i) === '<') {
          let tagEnd = formattedText.indexOf('>', i);
          if (tagEnd !== -1) {
            msgBubble.innerHTML += formattedText.substring(i, tagEnd + 1);
            i = tagEnd + 1;
          } else {
            msgBubble.innerHTML += formattedText.charAt(i);
            i++;
          }
        } 
        // Handle HTML Entities (e.g. &amp;) so they don't print letter-by-letter
        else if (formattedText.charAt(i) === '&') {
          let entEnd = formattedText.indexOf(';', i);
          if (entEnd !== -1 && (entEnd - i) < 10) { 
            msgBubble.innerHTML += formattedText.substring(i, entEnd + 1);
            i = entEnd + 1;
          } else {
            msgBubble.innerHTML += formattedText.charAt(i);
            i++;
          }
        } 
        // Normal characters
        else {
          msgBubble.innerHTML += formattedText.charAt(i);
          i++;
        }
        messagesEl.scrollTop = messagesEl.scrollHeight;
        
        // Randomize speed slightly for a more natural feel (10ms - 25ms)
        setTimeout(typeWriter, Math.random() * 15 + 10);
      } else {
        resolve();
      }
    }
    typeWriter();
  });
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

async function sendMessage(text) {
  text = (text || "").trim();
  if(!text || isThinking) return;

  emptyState.classList.add("d-none");
  messagesEl.classList.remove("d-none");

  addMessage(text, "user");
  textarea.value = "";
  sendBtn.disabled = true;
  isThinking = true;

  const typingRow = document.createElement("div");
  typingRow.className = "msg-row bot typing";
  typingRow.innerHTML = `<div class="msg"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>`;
  messagesEl.appendChild(typingRow);
  messagesEl.scrollTop = messagesEl.scrollHeight;

  const responseText = await fetchResponse(text);

  typingRow.remove();
  
  // Use the new typing effect for the bot's response
  await addTypingMessage(responseText, "bot");
  
  isThinking = false;
  sendBtn.disabled = !textarea.value.trim();
  textarea.focus();
}

// Reset Conversation
function resetChat() {
  messagesEl.innerHTML = '';
  messagesEl.classList.add('d-none');
  emptyState.classList.remove('d-none');
  textarea.value = '';
  sendBtn.disabled = true;
  document.querySelectorAll('.hist-item').forEach(x => x.classList.remove('active'));
}

// Event Listeners
textarea.addEventListener('input', () => {
  sendBtn.disabled = !textarea.value.trim() || isThinking;
});

sendBtn.addEventListener("click", ()=> sendMessage(textarea.value));
textarea.addEventListener("keydown", e=>{
  if(e.key === "Enter" && !e.shiftKey){
    e.preventDefault();
    sendMessage(textarea.value);
  }
});

newChatBtn?.addEventListener('click', resetChat);

closeBtn?.addEventListener('click', () => {
  window.location.href = '../dashboard_ui/index.html';
});

// Mode Switcher (Full-Screen ↔ Floating Widget)
toggleModeBtn.addEventListener('click', () => {
  const isFloating = chatApp.classList.toggle('mode-floating');
  chatApp.classList.toggle('mode-fullscreen', !isFloating);

  // Update toggle icon
  if (isFloating) {
    toggleIcon.classList.remove('fa-down-left-and-up-right-to-center');
    toggleIcon.classList.add('fa-up-right-and-down-left-from-center');
  } else {
    toggleIcon.classList.remove('fa-up-right-and-down-left-from-center');
    toggleIcon.classList.add('fa-down-left-and-up-right-to-center');
  }

  if (!isFloating) {
    chatApp.style.transform = '';
    xOffset = 0;
    yOffset = 0;
  }

  setTimeout(() => {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }, 100);
});

// Initialize on Load
renderRecentChats();
renderQuickPrompts();

// --- FLOATING WINDOW DRAG LOGIC ---
const topbar = document.querySelector('.ums-header');
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
  if (e.target.closest('button') || e.target.closest('a')) return;

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