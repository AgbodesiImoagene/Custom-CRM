function showProfile() {
    // Fetch and display user profile data
    fetchUserProfile();
    $('#profile-modal').modal('show');
}

function logout() {
    localStorage.removeItem('token');
    location.reload();
}

function confirmDeleteAccount() {
    $('#delete-account-modal').modal('show');
}

async function fetchUserProfile() {
    try {
        const response = await fetch(`${BASE_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch user profile');
        }

        const user = await response.json();
        populateProfileForm(user);
    } catch (error) {
        alert(error.message);
    }
}

function populateProfileForm(user) {
    const form = document.getElementById('profile-form');
    form.innerHTML = `
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" name="username" value="${user.username}" required>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" value="${user.email}" required>
        </div>
        <div class="form-group">
            <label for="phone">Phone</label>
            <input type="text" class="form-control" id="phone" name="phone" value="${user.phone}" required>
        </div>
        <div class="form-group">
            <label for="first_name">First Name</label>
            <input type="text" class="form-control" id="first_name" name="first_name" value="${user.first_name}" required>
        </div>
        <div class="form-group">
            <label for="last_name">Last Name</label>
            <input type="text" class="form-control" id="last_name" name="last_name" value="${user.last_name}" required>
        </div>
    `;
}

async function updateProfile() {
    const form = document.getElementById('profile-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const user_id = localStorage.getItem('user_id');

    try {
        const response = await fetch(`${BASE_URL}/users/${user_id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Failed to update profile');
        }

        $('#profile-modal').modal('hide');
        alert('Profile updated successfully');
    } catch (error) {
        alert(error.message);
    }
}

async function deleteAccount() {
    try {
        const response = await fetch(`${BASE_URL}/users/me`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to delete account');
        }

        localStorage.removeItem('token');
        location.reload();
    } catch (error) {
        alert(error.message);
    }
}