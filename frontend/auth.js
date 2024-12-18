document.querySelector('#login-form form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${BASE_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'username': username,
                'password': password,
            }),
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        localStorage.setItem('token', data.access_token);

        // Fetch user details to set user_id in local storage
        const userResponse = await fetch(`${BASE_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${data.access_token}`,
            },
        });

        if (!userResponse.ok) {
            throw new Error('Failed to fetch user details');
        }

        const user = await userResponse.json();
        localStorage.setItem('user_id', user.id);

        document.getElementById('login-form').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        document.getElementById('profile-icon').style.display = 'block';

        // Set up token refresh
        setTimeout(refreshToken, (data.expires_in - 60) * 1000); // Refresh token 1 minute before it expires

        // Fetch user details to check admin status
        await checkAdminStatus();

        // Fetch objects
        fetchObjects();
    } catch (error) {
        alert(error.message);
    }
});

document.querySelector('#signup-form form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const phone = document.getElementById('signup-phone').value;
    const firstName = document.getElementById('signup-first-name').value;
    const lastName = document.getElementById('signup-last-name').value;
    const password = document.getElementById('signup-password').value;

    // Simple validation
    if (!username || !email || !phone || !firstName || !lastName || !password) {
        alert('All fields are required');
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'username': username,
                'email': email,
                'phone': phone,
                'first_name': firstName,
                'last_name': lastName,
                'password': password,
            }),
        });

        if (!response.ok) {
            throw new Error('Sign-up failed');
        }

        alert('Sign-up successful! Please log in.');
        showLoginForm();
    } catch (error) {
        alert(error.message);
    }
});

async function refreshToken() {
    try {
        const response = await fetch(`${BASE_URL}/auth/token/refresh`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error('Token refresh failed');
        }

        const data = await response.json();
        localStorage.setItem('token', data.access_token);

        // Set up next token refresh
        setTimeout(refreshToken, (data.expires_in - 60) * 1000);
    } catch (error) {
        alert(error.message);
        // Optionally, redirect to login page
        document.getElementById('login-form').style.display = 'block';
        document.getElementById('dashboard').style.display = 'none';
    }
}

async function checkTokenValidity() {
    const token = localStorage.getItem('token');
    if (!token) return false;

    try {
        const response = await fetch(`${BASE_URL}/auth/token/verify`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.ok) {
            await checkAdminStatus();
        }

        return response.ok;
    } catch (error) {
        return false;
    }
}

async function checkAdminStatus() {
    const userResponse = await fetch(`${BASE_URL}/users/me`, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
    });

    if (userResponse.ok) {
        const user = await userResponse.json();
        const objectTypeSelect = document.getElementById('object-type');
        const usersOption = document.createElement('option');
        usersOption.value = 'users';
        usersOption.text = 'Users';

        if (user.role === 'admin') {
            objectTypeSelect.prepend(usersOption);
            document.getElementById('push-to-gong-button').style.display = 'block';
        } else {
            const existingUsersOption = objectTypeSelect.querySelector('option[value="users"]');
            if (existingUsersOption) {
                existingUsersOption.remove();
            }
            document.getElementById('push-to-gong-button').style.display = 'none';
        }
    }
}

function showSignUpForm() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('signup-form').style.display = 'block';
}

function showLoginForm() {
    document.getElementById('signup-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
}

// Check if the user is already logged in and the token is valid
checkTokenValidity().then(isValid => {
    if (isValid) {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        document.getElementById('profile-icon').style.display = 'block';

        // Fetch CRM objects
        fetchObjects();
    }
});