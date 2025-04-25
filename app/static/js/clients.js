document.addEventListener('DOMContentLoaded', () => {
    loadClients();
    
    // Search functionality
    document.getElementById('searchBtn').addEventListener('click', () => {
        const searchTerm = document.getElementById('searchInput').value;
        loadClients(searchTerm);
    });

    // Add new client
    document.getElementById('addClientBtn').addEventListener('click', showClientForm);
});

function loadClients(search = '') {
    fetch(`/api/clients/search?name=${search}`)
        .then(res => res.json())
        .then(clients => {
            const tbody = document.querySelector('#clientsTable tbody');
            tbody.innerHTML = clients.map(client => `
                <tr>
                    <td>${client.id}</td>
                    <td>${client.name}</td>
                    <td>${client.age}</td>
                    <td>${client.gender}</td>
                    <td>${client.programs.join(', ')}</td>
                    <td>
                        <button onclick="editClient(${client.id})">Edit</button>
                        <button onclick="deleteClient(${client.id})">Delete</button>
                    </td>
                </tr>
            `).join('');
        });
}

function showClientForm(client = null) {
    const modal = document.getElementById('clientModal');
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            <h3>${client ? 'Edit' : 'Add'} Client</h3>
            <form id="clientForm">
                <input type="hidden" name="id" value="${client?.id || ''}">
                <input type="text" name="name" placeholder="Full Name" value="${client?.name || ''}" required>
                <input type="number" name="age" placeholder="Age" value="${client?.age || ''}" required>
                <select name="gender" required>
                    <option value="">Select Gender</option>
                    <option value="male" ${client?.gender === 'male' ? 'selected' : ''}>Male</option>
                    <option value="female" ${client?.gender === 'female' ? 'selected' : ''}>Female</option>
                </select>
                <button type="submit">Save</button>
            </form>
        </div>
    `;
    modal.style.display = 'block';
    
    // Handle form submission
    document.getElementById('clientForm').addEventListener('submit', handleClientSubmit);
}

function handleClientSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const clientData = Object.fromEntries(formData);
    
    const method = clientData.id ? 'PUT' : 'POST';
    const url = clientData.id ? `/api/clients/${clientData.id}` : '/api/clients';
    
    fetch(url, {
        method,
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(clientData)
    })
    .then(() => {
        document.getElementById('clientModal').style.display = 'none';
        loadClients();
    });
}