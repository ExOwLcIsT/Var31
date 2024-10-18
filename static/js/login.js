document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const showLoginBtn = document.getElementById('show-login');
    const showRegisterBtn = document.getElementById('show-register');
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');
    const forgotPasswordBtn = document.getElementById('forgot-password-btn');

    showLoginBtn.addEventListener('click', function () {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
    });

    showRegisterBtn.addEventListener('click', function () {
        registerForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
    });

    loginBtn.addEventListener('click', async function () {
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('login-error').textContent = '';
            alert(data.message);
            window.location.href = "/";
        } else {
            document.getElementById('login-error').textContent = data.error;
        }
    });

    // Register function
    registerBtn.addEventListener('click', async function () {
        const username = document.getElementById('register-username').value;
        const password = document.getElementById('register-password').value;
        const accessRights = document.getElementById('register-access-rights').value;

        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password, access_rights: accessRights })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('register-error').textContent = '';
            alert(data.message);
            window.location.href = "/login";
        } else {
            document.getElementById('register-error').textContent = data.error;
        }
    });

    // Forgot password function
    forgotPasswordBtn.addEventListener('click', async function () {
        const username = document.getElementById('login-username').value;

        const response = await fetch('/api/login/forgot-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('forgot-password-response').textContent = `Ваш пароль: ${data.password}`;
        } else {
            document.getElementById('forgot-password-response').textContent = data.error;
        }
    });
});
