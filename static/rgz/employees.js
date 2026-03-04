let currentPage = 1;
let currentSearch = '';
let currentSort = 'id';
let currentOrder = 'asc';

function loadEmployees() {
    const loading = document.getElementById('loading');
    loading.style.display = 'block';
    
    const url = new URL('/rgz/api/employees', window.location.origin);
    url.searchParams.append('page', currentPage);
    url.searchParams.append('search', currentSearch);
    url.searchParams.append('sort_by', currentSort);
    url.searchParams.append('sort_order', currentOrder);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            renderTable(data.employees);
            renderPagination(data);
            loading.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            loading.style.display = 'none';
        });
}

function renderTable(employees) {
    const table = document.getElementById('employees-table');
    
    let html = `
        <table class="employees-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>ФИО</th>
                    <th>Должность</th>
                    <th>Пол</th>
                    <th>Телефон</th>
                    <th>Email</th>
                    <th>Исп. срок</th>
                    <th>Дата приема</th>
                    ${window.IS_AUTH ? '<th>Действия</th>' : ''}
                </tr>
            </thead>
            <tbody>
    `;
    
    employees.forEach(emp => {
        html += `
            <tr>
                <td>${emp.id}</td>
                <td><a href="/rgz/employee/${emp.id}">${emp.full_name}</a></td>
                <td>${emp.position}</td>
                <td>${emp.gender}</td>
                <td>${emp.phone}</td>
                <td>${emp.email}</td>
                <td>${emp.probation_text}</td>
                <td>${emp.hire_date}</td>
                ${window.IS_AUTH ? `
                <td class="actions">
                    <a href="/rgz/employee/${emp.id}/edit" class="btn-small">✏️</a>
                    <form method="POST" action="/rgz/employee/${emp.id}/delete" style="display:inline;" 
                          onsubmit="return confirm('Удалить сотрудника?')">
                        <button type="submit" class="btn-small delete">🗑️</button>
                    </form>
                </td>
                ` : ''}
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    table.innerHTML = html;
}

function renderPagination(data) {
    const pagination = document.getElementById('pagination');
    let html = '';
    
    if (data.pages > 1) {
        if (data.page > 1) {
            html += `<button onclick="goToPage(${data.page - 1})">← Пред.</button>`;
        }
        
        html += `<span>Страница ${data.page} из ${data.pages}</span>`;
        
        if (data.page < data.pages) {
            html += `<button onclick="goToPage(${data.page + 1})">След. →</button>`;
        }
    }
    
    pagination.innerHTML = html;
}

function goToPage(page) {
    currentPage = page;
    loadEmployees();
}

// Поиск
document.getElementById('search-btn').addEventListener('click', () => {
    currentSearch = document.getElementById('search-input').value;
    currentPage = 1;
    loadEmployees();
});

document.getElementById('search-input').addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        currentSearch = e.target.value;
        currentPage = 1;
        loadEmployees();
    }
});

// Сортировка
document.getElementById('sort-select').addEventListener('change', e => {
    currentSort = e.target.value;
    currentPage = 1;
    loadEmployees();
});

document.getElementById('sort-order').addEventListener('click', e => {
    currentOrder = currentOrder === 'asc' ? 'desc' : 'asc';
    e.target.textContent = currentOrder === 'asc' ? '↑ По возрастанию' : '↓ По убыванию';
    currentPage = 1;
    loadEmployees();
});

// Первоначальная загрузка
document.addEventListener('DOMContentLoaded', loadEmployees);