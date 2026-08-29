// ==========================================================================
// UMS DASHBOARD - MAIN SCRIPT
// ==========================================================================

// --- THEME TOGGLE LOGIC ---
const themeToggleBtn = document.getElementById('theme-toggle');
const rootElement = document.documentElement;
const themeIcon = themeToggleBtn.querySelector('i');

// Check local storage for saved theme, default to 'light'
const savedTheme = localStorage.getItem('ums-theme') || 'light';
rootElement.setAttribute('data-theme', savedTheme);
updateThemeIcon(savedTheme);

// --- FETCH DYNAMIC DASHBOARD DATA ---
async function fetchDashboardData() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '../login_ui/index.html';
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/dashboard', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Failed to fetch dashboard data");
        const data = await response.json();

        // Hydrate Profile
        if (data.profile) {
            document.getElementById('headerName').textContent = data.profile.name;
            document.getElementById('welcomeName').textContent = data.profile.name;
            document.getElementById('dropdownName').textContent = data.profile.name;
            document.getElementById('dropdownBranch').textContent = `B.Tech ${data.profile.branch}`;
            document.getElementById('semesterBadge').textContent = `Semester ${data.profile.semester}`;
        }

        // Hydrate Attendance
        if (data.attendance) {
            const overall = data.attendance.overall_percentage;
            document.getElementById('overallAttendance').textContent = overall;
            
            const badge = document.getElementById('attendanceBadge');
            if (overall >= 75) { badge.textContent = 'Good'; badge.className = 'badge bg-success fs-7 ms-2 align-middle border-0'; }
            else if (overall >= 60) { badge.textContent = 'Warning'; badge.className = 'badge bg-warning text-dark fs-7 ms-2 align-middle border-0'; }
            else { badge.textContent = 'Critical'; badge.className = 'badge bg-danger fs-7 ms-2 align-middle border-0'; }

            const tbody = document.getElementById('attendanceBody');
            tbody.innerHTML = '';
            data.attendance.subjects.forEach(sub => {
                const color = sub.percentage >= 75 ? '#28a745' : (sub.percentage >= 60 ? '#ffc107' : '#dc3545');
                tbody.innerHTML += `
                    <tr class="border-bottom header-border">
                        <td class="py-2 ps-0"><span class="fw-bold">${sub.subject_code}</span> <span class="text-muted">(${sub.subject_name})</span></td>
                        <td class="py-2 text-end"><strong style="color: ${color};">${sub.percentage}%</strong></td>
                    </tr>
                `;
            });
        }

        // Hydrate Timetable
        if (data.timetable && data.timetable.classes && data.timetable.classes.length > 0) {
            const schedDiv = document.getElementById('mon-schedule');
            schedDiv.innerHTML = '';
            data.timetable.classes.forEach(cls => {
                schedDiv.innerHTML += `
                    <div class="row g-2 align-items-center py-3 border-bottom header-border schedule-row">
                        <div class="col-3"><span class="schedule-time-badge">${cls.start_time}</span></div>
                        <div class="col-6"><span class="fw-bold fs-6 d-block">${cls.subject}</span></div>
                        <div class="col-3 text-end"><span class="text-muted fs-6">${cls.room}</span></div>
                    </div>
                `;
            });
        } else {
            document.getElementById('mon-schedule').innerHTML = '<div class="py-3 text-muted">No classes scheduled for today!</div>';
        }

        // Hydrate RMS
        if (data.rms) {
            let pending = 0, progress = 0, closed = 0;
            const statusMap = { 'Pending': 'Pending', 'In Progress': 'progress', 'Resolved': 'closed' };
            // Simple count if the backend returned an array of tickets
            if (Array.isArray(data.rms)) {
                data.rms.forEach(ticket => {
                    if (ticket.status === 'Pending') pending++;
                    else if (ticket.status === 'In Progress') progress++;
                    else closed++;
                });
            } else if (typeof data.rms === 'string' && data.rms.includes('no recent')) {
                // Do nothing, all 0
            }
            
            document.getElementById('rmsPending').textContent = String(pending).padStart(2, '0');
            document.getElementById('rmsProgress').textContent = String(progress).padStart(2, '0');
            document.getElementById('rmsClosed').textContent = String(closed).padStart(2, '0');
        }
    } catch (err) {
        console.error(err);
    }
}

// Call on load
document.addEventListener('DOMContentLoaded', fetchDashboardData);

themeToggleBtn.addEventListener('click', () => {
    const currentTheme = rootElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    rootElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('ums-theme', newTheme);
    updateThemeIcon(newTheme);
});

function updateThemeIcon(theme) {
    if (theme === 'dark') {
        themeIcon.classList.remove('bi-moon-fill');
        themeIcon.classList.add('bi-sun-fill');
    } else {
        themeIcon.classList.remove('bi-sun-fill');
        themeIcon.classList.add('bi-moon-fill');
    }
}


// --- MAP NAVIGATION LOGIC (REAL GOOGLE MAPS) ---
window.highlightMapBlock = function (searchQuery) {
    const mapIframe = document.getElementById('lpu-map');
    if (mapIframe) {
        // Generates the proper Google Maps embed URL
        mapIframe.src = `https://maps.google.com/maps?q=${encodeURIComponent(searchQuery)}&t=&z=16&ie=UTF8&iwloc=&output=embed`;
        console.log(`Navigation: Updating map to ${searchQuery}`);
    }
};

window.scrollToAndHighlight = function (searchQuery) {
    // Pick a random LPU landmark if requested
    if (searchQuery === 'random') {
        const locations = [
            'Baldev Raj Mittal Unipolis, Lovely Professional University',
            'LPU Main Gate, Phagwara',
            'Block 34, Lovely Professional University',
            'Shanti Devi Mittal Auditorium, LPU'
        ];
        searchQuery = locations[Math.floor(Math.random() * locations.length)];
    }

    // Smooth scroll to the map section
    const mapSection = document.getElementById('map-section');
    if (mapSection) {
        const yOffset = -100; // Account for the fixed navbar
        const y = mapSection.getBoundingClientRect().top + window.scrollY + yOffset;
        window.scrollTo({ top: y, behavior: 'smooth' });
    }

    // Wait for the scroll to finish, then reload the map to the new location
    setTimeout(() => {
        window.highlightMapBlock(searchQuery);
    }, 600);
};


// --- NLP FEATURE OFFCANVAS LOGIC ---
const botFeatures = {
    'timetable': {
        icon: '<i class="bi bi-calendar3 me-2 accent-icon"></i>',
        title: 'Timetable & Faculty Status',
        desc: 'Instantly check your daily schedule, identify free slots, and verify if a teacher is on leave before walking to class.',
        prompts: [
            "What are my classes for today?",
            "Is the CSE316 teacher on leave today?",
            "When is my next free slot?"
        ]
    },
    'attendance': {
        icon: '<i class="bi bi-person-check me-2 accent-icon"></i>',
        title: 'Predictive Attendance',
        desc: 'Track current attendance and predict percentage drops before deciding to skip a class.',
        prompts: [
            "What is my current overall attendance?",
            "If I leave the Computer Network class today, how much will my percentage decrease?",
            "How many more classes can I miss in CSE202?"
        ]
    },
    'exams': {
        icon: '<i class="bi bi-pencil-square me-2 accent-icon"></i>',
        title: 'Exam Intelligence',
        desc: 'Retrieve syllabus details, course outcomes, and subject credit weights instantly.',
        prompts: [
            "Show me the syllabus for Mid-Terms in AI/ML.",
            "How many credits is the Database Management subject?",
            "What are the Course Outcomes (COs) for CSE316?"
        ]
    },
    'fees': {
        icon: '<i class="bi bi-wallet2 me-2 accent-icon"></i>',
        title: 'Fee Breakdown',
        desc: 'Check pending dues with exact breakdowns across residential, semester, and examination categories.',
        prompts: [
            "How much are my total pending dues?",
            "Is my hostel residential fee cleared for this semester?",
            "Give me a breakdown of my examination fees."
        ]
    },
    'notifications': {
        icon: '<i class="bi bi-bell me-2 accent-icon"></i>',
        title: 'Smart Message Search',
        desc: 'Stop scrolling through endless uni messages. Search specific categories instantly.',
        prompts: [
            "Find messages related to Placement Drives.",
            "Show me the latest updates on the CDP project.",
            "Are there any urgent admin messages today?"
        ]
    },
    'announcements': {
        icon: '<i class="bi bi-megaphone me-2 accent-icon"></i>',
        title: 'Placement Eligibility',
        desc: 'Automatically cross-references your current CGPA/TGPA with placement announcements and allows instant registration.',
        prompts: [
            "Am I eligible for the upcoming Amazon placement drive?",
            "Show me drives matching my 8.5 CGPA.",
            "Register me for the Capgemini Brand Quest."
        ]
    },
    'hostel': {
        icon: '<i class="bi bi-house-door me-2 accent-icon"></i>',
        title: 'One-Prompt Leaves',
        desc: 'Apply for hostel or campus leave conversationally without filling out complex forms.',
        prompts: [
            "Apply for hostel leave from this Friday to Monday.",
            "I need a campus pass for tomorrow evening.",
            "What is the status of my weekend leave request?"
        ]
    },
    'rms': {
        icon: '<i class="bi bi-ticket-detailed me-2 accent-icon"></i>',
        title: 'Guided RMS Logging',
        desc: 'The bot guides you through categories, sub-categories, and problem details to log maintenance requests effortlessly.',
        prompts: [
            "I need to raise an RMS ticket for maintenance.",
            "My hostel room fan is broken.",
            "Check the status of my previous Wi-Fi complaint."
        ]
    },
    'library': {
        icon: '<i class="bi bi-book me-2 accent-icon"></i>',
        title: 'Library Locator',
        desc: 'Search for books by topic and get real-time availability and exact floor/shelf locations.',
        prompts: [
            "Show me available books related to the Stock Market.",
            "Is 'Clean Code' currently available?",
            "Which floor has books on Machine Learning?"
        ]
    },
    'cgpa': {
        icon: '<i class="bi bi-calculator me-2 accent-icon"></i>',
        title: 'Predictive CGPA Calc',
        desc: 'Input your CA and Mid-term scores, and the bot calculates exactly what you need in the End-term to secure a specific grade.',
        prompts: [
            "I got 25/30 in CA and 18/20 in Mid-term. What do I need in End-term for an 'O' grade?",
            "Predict my overall CGPA if I score 80% this semester.",
            "How much do I need to score to maintain a 9.0 TGPA?"
        ]
    }
};

window.showFeatureDetails = function (featureKey) {
    const data = botFeatures[featureKey];
    if (!data) return;

    document.getElementById('panelTitle').innerHTML = data.icon + data.title;
    document.getElementById('panelDesc').innerText = data.desc;

    const promptsContainer = document.getElementById('panelPrompts');
    promptsContainer.innerHTML = '';

    data.prompts.forEach(prompt => {
        const bubble = document.createElement('div');
        bubble.className = 'p-3 rounded-4 fs-7 mb-2 shadow-sm';
        bubble.style.backgroundColor = 'rgba(248, 204, 156, 0.15)';
        bubble.style.border = '1px solid var(--border-color)';
        bubble.innerHTML = `"${prompt}"`;
        promptsContainer.appendChild(bubble);
    });
};

// --- LOGOUT LOGIC ---
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        // Remove token from local storage
        localStorage.removeItem('token');
        // Redirect to login page
        window.location.href = '../login_ui/index.html';
    });
}