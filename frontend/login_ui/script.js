document.addEventListener("DOMContentLoaded", () => {

    /* =================================================
       GET ELEMENTS
    ================================================= */

    const passwordInput = document.getElementById("password");

    const togglePassword = document.getElementById("togglePassword");

    const loginForm = document.getElementById("loginForm");

    const registrationInput = document.getElementById("registration_id");


    /* =================================================
       PASSWORD SHOW / HIDE
    ================================================= */

    if (togglePassword && passwordInput) {

        togglePassword.addEventListener("click", () => {

            const isPassword = passwordInput.getAttribute("type") === "password";

            if (isPassword) {
                passwordInput.setAttribute("type", "text");
                togglePassword.textContent = "Hide";
            } else {
                passwordInput.setAttribute("type", "password");
                togglePassword.textContent = "Show";
            }
        });

        /* Allow Enter/Space keyboard interaction */
        togglePassword.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                togglePassword.click();
            }
        });
    }

    /* =================================================
       LOGIN FORM VALIDATION & BACKEND CONNECTION
    ================================================= */

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {

            // Prevent default HTML form submission
            event.preventDefault();

            const registrationId = registrationInput.value.trim();
            const password = passwordInput.value.trim();

            /* Check empty fields */
            if (!registrationId || !password) {
                alert("Please enter both your Registration ID and Password.");
                return;
            }

            try {
                const response = await fetch('http://localhost:5000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    // We map registrationId to registration_number for the backend
                    body: JSON.stringify({ registration_number: registrationId, password: password })
                });

                const data = await response.json();

                if (response.ok) {
                    // Save token and redirect
                    localStorage.setItem('token', data.access_token);
                    window.location.href = '../dashboard_ui/index.html';
                } else {
                    alert(data.msg || 'Login failed');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Network error. Ensure backend is running.');
            }
        });
    }

    /* =================================================
       DEMO LOGIN FUNCTIONALITY
    ================================================= */
    const demoLoginBtn = document.getElementById("demoLoginBtn");
    if (demoLoginBtn) {
        demoLoginBtn.addEventListener("click", () => {
            // Auto-fill credentials
            if (registrationInput) registrationInput.value = "DEMO-USER";
            if (passwordInput) passwordInput.value = "demo123";

            // Directly log in without backend validation
            localStorage.setItem('token', 'demo-token-12345');
            window.location.href = '../dashboard_ui/index.html';
        });
    }

});
