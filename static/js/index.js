function goToLogin() {
    window.location.href = "/login";
}

function showLoginRegisterButtons() {
    document.getElementById("login-btn").style.display = 'block';
    document.getElementById("logout-btn").style.display = 'none';
}
async function logout() {
    const response = await fetch('/api/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    if (response.ok) {
        document.cookie = 'logged_in_user=;expires=Thu, 01 Jan 1970 00:00:00 UTC;';
        location.reload();
    }
}

function showLogoutButton() {
    document.getElementById("login-btn").style.display = 'none';
    document.getElementById("logout-btn").style.display = 'block';
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
async function loadPage() {
    await loadCollections();

    document.getElementById('collection-select').addEventListener('change', function () {
        const selectedCollection = this.value;
        loadDocuments(selectedCollection);
        loadFieldsForRename();
        loadFieldsForDocument();
    });
    loadDocuments(document.getElementById('collection-select').value)

    const loggedInUser = getCookie('logged_in_user');
    if (loggedInUser) {
        showLogoutButton(loggedInUser);
    } else {
        showLoginRegisterButtons();
    }
    loadFieldsForRename();
    loadFieldsForDocument();
}
loadPage()