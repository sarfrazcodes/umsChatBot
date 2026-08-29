/* ===== DATA (replace with API/DB calls — see requirements.md) ===== */
const subjects = [
  {code:"CSE316", name:"Operating Systems", pct:87.5},
  {code:"INT221", name:"Full Stack Web Dev", pct:89.4},
  {code:"CSE320", name:"AI & Machine Learning", pct:78.5},
  {code:"MTH302", name:"Engineering Mathematics", pct:83.3},
];
const schedule = {
  "Mon29":[{time:"09:00 AM",code:"CSE316",name:"Operating Systems",room:"Block 14 · Room 302",color:"#ff5a2c"},
           {time:"10:00 AM",code:"INT221",name:"Full Stack Web Dev",room:"Block 32 · Lab 4",color:"#0d9488"},
           {time:"11:00 AM",code:"CSE320",name:"AI & Machine Learning",room:"Block 34 · Room 201",color:"#eab308"}],
  "Tue30":[{time:"09:00 AM",code:"MTH302",name:"Engineering Mathematics",room:"Block 10 · Room 110",color:"#6d5bd0"}],
  "Wed31":[{time:"11:00 AM",code:"CSE316",name:"Operating Systems Lab",room:"Block 14 · Lab 2",color:"#ff5a2c"}],
  "Thu01":[{time:"09:00 AM",code:"CSE320",name:"AI & Machine Learning",room:"Block 34 · Room 201",color:"#eab308"}],
  "Fri02":[{time:"10:00 AM",code:"INT221",name:"Full Stack Web Dev",room:"Block 32 · Lab 4",color:"#0d9488"}],
};
const quickAccess = [
  {icon:"fa-regular fa-calendar",title:"Timetable",sub:"View your week",active:true},
  {icon:"fa-regular fa-square-check",title:"Attendance",sub:"Track your progress"},
  {icon:"fa-solid fa-pen-ruler",title:"Exams",sub:"Dates & hall tickets"},
  {icon:"fa-regular fa-envelope",title:"Fees",sub:"Payments & receipts"},
  {icon:"fa-regular fa-bell",title:"Notifications",sub:"Stay in the loop"},
  {icon:"fa-solid fa-bullhorn",title:"Announcements",sub:"Campus updates"},
  {icon:"fa-solid fa-book",title:"Library",sub:"Books & renewals"},
  {icon:"fa-solid fa-house",title:"Hostel",sub:"Room & requests"},
];
const days = [{d:"Mon",n:29},{d:"Tue",n:30},{d:"Wed",n:31},{d:"Thu",n:1},{d:"Fri",n:2}];

/* ===== RENDER ===== */
document.getElementById("today-date").textContent = new Date().toDateString();

document.getElementById("subjects").innerHTML = subjects.map(s=>`
  <div class="subject-row py-2">
    <div class="d-flex justify-content-between"><span class="fw-semibold">${s.code} <span class="text-muted fw-normal">${s.name}</span></span><span class="fw-semibold">${s.pct}%</span></div>
    <div class="progress mt-1"><div class="progress-bar progress-bar-green" style="width:${s.pct}%"></div></div>
  </div>`).join("");

function renderDays(active){
  document.getElementById("day-tabs").innerHTML = days.map(x=>{
    const key = x.d+String(x.n).padStart(2,"0");
    return `<button class="day-tab ${key===active?'active':''}" onclick="selectDay('${key}')">
      <div class="d">${x.d}</div><div class="n">${String(x.n).padStart(2,"0")}</div></button>`;
  }).join("");
}
function renderClasses(key){
  const list = schedule[key] || [];
  document.getElementById("classes").innerHTML = list.length ? list.map(c=>`
    <div class="class-row py-3 d-flex align-items-center gap-3">
      <div class="class-bar" style="background:${c.color}"></div>
      <div class="text-muted-sm" style="width:80px">${c.time}</div>
      <div class="flex-grow-1"><div class="fw-bold">${c.code}</div><div class="text-muted-sm">${c.name}</div></div>
      <div class="text-muted-sm d-flex align-items-center gap-1"><i class="fa-regular fa-calendar"></i>${c.room}</div>
      <i class="fa-solid fa-chevron-right text-muted small"></i>
    </div>`).join("") : `<div class="text-muted-sm py-4 text-center">No classes scheduled.</div>`;
}
function selectDay(key){ renderDays(key); renderClasses(key); }
selectDay("Mon29");

document.getElementById("quick-access").innerHTML = quickAccess.map(q=>`
  <div class="col-6 col-md-3">
    <div class="qa-item p-3 d-flex align-items-center gap-2 ${q.active?'active-item':''}" role="button">
      <span class="qa-icon" style="background:#ffe3d5;color:var(--accent)"><i class="${q.icon}"></i></span>
      <div><div class="fw-semibold small">${q.title}</div><div class="text-muted-sm">${q.sub}</div></div>
    </div>
  </div>`).join("");

// Logout Functionality
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", (e) => {
    e.preventDefault();
    localStorage.removeItem("token"); // or whatever key is used for auth
    window.location.href = "../login_ui/index.html";
  });
}

// Session expiration logic
function checkSession() {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "../login_ui/index.html";
    return;
  }
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    // payload.exp is in seconds, Date.now() is in milliseconds
    if (payload.exp * 1000 < Date.now()) {
      localStorage.removeItem("token");
      window.location.href = "../login_ui/index.html";
    }
  } catch (e) {
    console.error("Invalid token format", e);
  }
}

// Check immediately on load, and then every minute
checkSession();
setInterval(checkSession, 60000);