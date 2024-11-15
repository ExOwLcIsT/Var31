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


async function access() {
    const response = await fetch('/api/role');

    let data = await response.json();
    console.log(data)
    let elements = []
    switch (data.role) {
        case "owner":
            console.log("yes")
             elements = document.getElementsByClassName("owner_access");
            for (var i = 0; i < elements.length; i++) {
                elements[i].style.display = "block";
            }
        case "admin":
            elements = document.getElementsByClassName("admin_access");
            for (var i = 0; i < elements.length; i++) {
                elements[i].style.display = "block";
            }
        case "operator":
            elements = document.getElementsByClassName("operator_access");
            for (var i = 0; i < elements.length; i++) {
                elements[i].style.display = "block";
            }
    }



}


async function loadPage() {
    await loadCollections();

    document.getElementById('collection-select').addEventListener('change', function () {
        const selectedCollection = this.value;
        loadDocuments(selectedCollection);
        loadFieldsForRename();
        loadFieldsForDocument();
        access()
    });
    await loadDocuments(document.getElementById('collection-select').value)

    const loggedInUser = getCookie('logged_in_user');
    if (loggedInUser) {
        showLogoutButton(loggedInUser);
    } else {
        showLoginRegisterButtons();
    }
    await loadFieldsForRename();
    await loadFieldsForDocument();
    await access();
}
loadPage()