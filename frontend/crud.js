async function fetchObjects() {
    const objectType = document.getElementById('object-type').value;
    try {
        const response = await fetch(`${BASE_URL}/${objectType}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch ${objectType}`);
        }

        const objects = await response.json();
        const tbody = document.getElementById('crm-objects');
        tbody.innerHTML = '';

        const currentUser = await fetchCurrentUser();

        objects.forEach(object => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${object.id}</td>
                <td>${object.name || object.title || object.first_name + ' ' + object.last_name || object.username}</td>
                <td>
                    ${objectType === 'users' ? `
                        ${object.role != 'admin' ? `<button class="btn btn-primary" onclick="promoteUser(${object.id})">Promote</button>` : ''}
                        <button class="btn btn-secondary" onclick="toggleUserStatus(${object.id}, ${object.disabled})">${object.disabled ? 'Enable' : 'Disable'}</button>
                    ` : `
                        ${(currentUser.role === 'admin' || object.owner_id === currentUser.id) ? `
                            <button class="btn btn-primary" onclick="editObject('${objectType}', ${object.id})"><i class="fas fa-edit"></i></button>
                            <button class="btn btn-danger" onclick="deleteObject('${objectType}', ${object.id})"><i class="fas fa-trash-alt"></i></button>
                        ` : ''}
                    `}
                </td>
            `;
            tr.style.cursor = 'pointer';
            tr.addEventListener('click', (event) => {
                if (!event.target.closest('button')) {
                    showObjectDetails(objectType, object.id);
                }
            });
            tbody.appendChild(tr);
        });
    } catch (error) {
        alert(error.message);
    }
}

async function fetchCurrentUser() {
    const response = await fetch(`${BASE_URL}/users/me`, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
    });

    if (!response.ok) {
        throw new Error('Failed to fetch current user');
    }

    return await response.json();
}

document.querySelector('#crud-form form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const objectType = document.getElementById('object-type').value;
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    // Remove empty fields
    for (const key in data) {
        if (data[key] === '') {
            delete data[key];
        }
    }

    if (objectType === 'leads' || objectType === 'deals') {
        data.owner_id = localStorage.getItem('user_id');
    }

    try {
        const method = data.id ? 'PUT' : 'POST';
        const url = data.id ? `${BASE_URL}/${objectType}/${data.id}` : `${BASE_URL}/${objectType}`;

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`Failed to save ${objectType}`);
        }

        hideCrudForm();
        fetchObjects();
    } catch (error) {
        alert(error.message);
    }
});

async function editObject(objectType, id) {
    try {
        const response = await fetch(`${BASE_URL}/${objectType}/${id}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch ${objectType}`);
        }

        const object = await response.json();
        populateForm(objectType, object);
        document.getElementById('crud-form-title').innerText = `Edit ${objectType}`;
        document.getElementById('crud-form').style.display = 'block';
    } catch (error) {
        alert(error.message);
    }
}

async function deleteObject(objectType, id) {
    try {
        const response = await fetch(`${BASE_URL}/${objectType}/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to delete ${objectType}`);
        }

        fetchObjects();
    } catch (error) {
        alert(error.message);
    }
}

async function showObjectDetails(objectType, id) {
    try {
        const response = await fetch(`${BASE_URL}/${objectType}/${id}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch ${objectType}`);
        }

        const object = await response.json();
        const detailsBody = document.getElementById('object-details-body');
        detailsBody.innerHTML = '';

        for (const [key, value] of Object.entries(object)) {
            const p = document.createElement('p');
            if (key === 'domains') {
                p.textContent = `${key}: ${value.map(domain => domain.name).join(', ')}`;
            } else {
                p.textContent = `${key}: ${value}`;
            }
            detailsBody.appendChild(p);
        }

        $('#object-details-modal').modal('show');
    } catch (error) {
        alert(error.message);
    }
}

function showCreateForm() {
    const objectType = document.getElementById('object-type').value;
    populateForm(objectType, {});
    document.getElementById('crud-form-title').innerText = 'Create New Object';
    document.getElementById('crud-form').style.display = 'block';
}

function hideCrudForm() {
    document.getElementById('crud-form').style.display = 'none';
}

async function populateForm(objectType, object) {
    const formContent = document.getElementById('crud-form-content');
    formContent.innerHTML = '';

    if (objectType === 'companies') {
        formContent.innerHTML = `
            <input type="hidden" name="id" value="${object.id || ''}">
            <div class="form-group">
                <label for="name">Name</label>
                <input type="text" class="form-control" name="name" value="${object.name || ''}" required>
            </div>
            <div class="form-group">
                <label for="industry">Industry</label>
                <select class="form-control" name="industry" required>
                    ${Object.values(IndustryEnum).map(industry => `
                        <option value="${industry}" ${object.industry === industry ? 'selected' : ''}>${industry}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-group">
                <label for="domains">Domains</label>
                <div id="domains-container">
                    ${(object.domains || []).map(domain => `
                        <div class="input-group mb-2">
                            <input type="text" class="form-control" name="domains[]" value="${domain.name}" required>
                            <button type="button" class="btn btn-danger" onclick="removeDomain(this)">Remove</button>
                        </div>
                    `).join('')}
                </div>
                <button type="button" class="btn btn-secondary" onclick="addDomain()">Add Domain</button>
            </div>
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" class="btn btn-secondary" onclick="hideCrudForm()">Cancel</button>
        `;
    } else if (objectType === 'contacts') {
        const companies = await fetchCompanies();
        formContent.innerHTML = `
            <input type="hidden" name="id" value="${object.id || ''}">
            <div class="form-group">
                <label for="first_name">First Name</label>
                <input type="text" class="form-control" name="first_name" value="${object.first_name || ''}" required>
            </div>
            <div class="form-group">
                <label for="last_name">Last Name</label>
                <input type="text" class="form-control" name="last_name" value="${object.last_name || ''}" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" class="form-control" name="email" value="${object.email || ''}" required>
            </div>
            <div class="form-group">
                <label for="phone">Phone</label>
                <input type="text" class="form-control" name="phone" value="${object.phone || ''}" required>
            </div>
            <div class="form-group">
                <label for="company_id">Company</label>
                <select class="form-control" name="company_id" required>
                    ${companies.map(company => `
                        <option value="${company.id}" ${object.company_id === company.id ? 'selected' : ''}>${company.name}</option>
                    `).join('')}
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" class="btn btn-secondary" onclick="hideCrudForm()">Cancel</button>
        `;
    } else if (objectType === 'leads') {
        const companies = await fetchCompanies();
        const contacts = await fetchContacts();
        const deals = await fetchDeals();
        formContent.innerHTML = `
            <input type="hidden" name="id" value="${object.id || ''}">
            <div class="form-group">
                <label for="first_name">First Name</label>
                <input type="text" class="form-control" name="first_name" value="${object.first_name || ''}" required>
            </div>
            <div class="form-group">
                <label for="last_name">Last Name</label>
                <input type="text" class="form-control" name="last_name" value="${object.last_name || ''}" required>
            </div>
            <div class="form-group">
                <label for="company">Company</label>
                <input type="text" class="form-control" name="company" value="${object.company || ''}" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" class="form-control" name="email" value="${object.email || ''}" required>
            </div>
            <div class="form-group">
                <label for="phone">Phone</label>
                <input type="text" class="form-control" name="phone" value="${object.phone || ''}" required>
            </div>
            <div class="form-group">
                <label for="details">Details</label>
                <textarea class="form-control" name="details">${object.details || ''}</textarea>
            </div>
            <div class="form-group">
                <label for="status">Status</label>
                <select class="form-control" name="status" required>
                    ${Object.values(LeadStatusEnum).map(status => `
                        <option value="${status}" ${object.status === status ? 'selected' : ''}>${status}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-group">
                <label for="company_id">Converted to Company</label>
                <select class="form-control" name="company_id" required>
                    ${companies.map(company => `
                        <option value="${company.id}" ${object.company_id === company.id ? 'selected' : ''}>${company.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-group">
                <label for="contact_id">Converted to Contact</label>
                <select class="form-control" name="contact_id" required>
                    ${contacts.map(contact => `
                        <option value="${contact.id}" ${object.contact_id === contact.id ? 'selected' : ''}>${contact.first_name} ${contact.last_name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-group">
                <label for="deal_id">Converted to Deal</label>
                <select class="form-control" name="deal_id" required>
                    ${deals.map(deal => `
                        <option value="${deal.id}" ${object.deal_id === deal.id ? 'selected' : ''}>${deal.title}</option>
                    `).join('')}
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" class="btn btn-secondary" onclick="hideCrudForm()">Cancel</button>
        `;
    } else if (objectType === 'deals') {
        const companies = await fetchCompanies();
        formContent.innerHTML = `
            <input type="hidden" name="id" value="${object.id || ''}">
            <div class="form-group">
                <label for="title">Title</label>
                <input type="text" class="form-control" name="title" value="${object.title || ''}" required>
            </div>
            <div class="form-group">
                <label for="amount">Amount</label>
                <input type="number" class="form-control" name="amount" value="${object.amount || ''}" required>
            </div>
            <div class="form-group">
                <label for="open_date">Open Date</label>
                <input type="date" class="form-control" name="open_date" value="${object.open_date ? object.open_date.split('T')[0] : ''}" required>
            </div>
            <div class="form-group">
                <label for="close_date">Close Date</label>
                <input type="date" class="form-control" name="close_date" value="${object.close_date ? object.close_date.split('T')[0] : ''}">
            </div>
            <div class="form-group">
                <label for="company_id">Company</label>
                <select class="form-control" name="company_id" required>
                    ${companies.map(company => `
                        <option value="${company.id}" ${object.company_id === company.id ? 'selected' : ''}>${company.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-group">
                <label for="stage">Stage</label>
                <select class="form-control" name="stage" required>
                    ${Object.values(StageEnum).map(stage => `
                        <option value="${stage}" ${object.stage === stage ? 'selected' : ''}>${stage}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-group">
                <label for="description">Description</label>
                <textarea class="form-control" name="description">${object.description || ''}</textarea>
            </div>
            <div class="form-group">
                <label for="status">Status</label>
                <select class="form-control" name="status" required>
                    ${Object.values(StatusEnum).map(status => `
                        <option value="${status}" ${object.status === status ? 'selected' : ''}>${status}</option>
                    `).join('')}
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" class="btn btn-secondary" onclick="hideCrudForm()">Cancel</button>
        `;
    }
}

async function fetchCompanies() {
    try {
        const response = await fetch(`${BASE_URL}/companies`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch companies');
        }

        return await response.json();
    } catch (error) {
        alert(error.message);
        return [];
    }
}

async function fetchContacts() {
    try {
        const response = await fetch(`${BASE_URL}/contacts`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch contacts');
        }

        return await response.json();
    } catch (error) {
        alert(error.message);
        return [];
    }
}

async function fetchDeals() {
    try {
        const response = await fetch(`${BASE_URL}/deals`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch deals');
        }

        return await response.json();
    } catch (error) {
        alert(error.message);
        return [];
    }
}

function addDomain() {
    const domainsContainer = document.getElementById('domains-container');
    const domainInput = document.createElement('div');
    domainInput.className = 'input-group mb-2';
    domainInput.innerHTML = `
        <input type="text" class="form-control" name="domains[]" required>
        <button type="button" class="btn btn-danger" onclick="removeDomain(this)">Remove</button>
    `;
    domainsContainer.appendChild(domainInput);
}

function removeDomain(button) {
    button.parentElement.remove();
}

async function promoteUser(userId) {
    try {
        const response = await fetch(`${BASE_URL}/users/promote/${userId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to promote user');
        }

        fetchObjects();
    } catch (error) {
        alert(error.message);
    }
}

async function toggleUserStatus(userId, isDisabled) {
    try {
        const endpoint = isDisabled ? 'enable' : 'disable';
        const response = await fetch(`${BASE_URL}/users/${endpoint}/${userId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to ${isDisabled ? 'enable' : 'disable'} user`);
        }

        fetchObjects();
    } catch (error) {
        alert(error.message);
    }
}

function toggleCreateButton() {
    const objectType = document.getElementById('object-type').value;
    const createButton = document.getElementById('create-button');
    if (objectType === 'users') {
        createButton.style.display = 'none';
    } else {
        createButton.style.display = 'block';
    }
}