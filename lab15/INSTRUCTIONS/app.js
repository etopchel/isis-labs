/* Занятие 14. Клиентская логика для работы с API. */
const API = "http://localhost:5000/api";
let editingId = null;
 
// Загрузка списка студентов
async function loadStudents() {
    const resp = await fetch(`${API}/students`);
    const students = await resp.json();
    const tbody = document.getElementById("students-table");
 
    tbody.innerHTML = students.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.last_name}</td>
            <td>${s.first_name}</td>
            <td>${s.group_name || '---'}</td>
            <td>${s.email || '---'}</td>
            <td>
                <button class='btn btn-edit'
                    onclick='editStudent(${s.id})'>Изм.</button>
                <button class='btn btn-delete'
                    onclick='deleteStudent(${s.id})'>Удал.</button>
            </td>
        </tr>
    `).join("");
}
 
// Показать/скрыть форму
function showForm() {
    document.getElementById("form-panel").style.display = "block";
    document.getElementById("form-title").textContent =
        editingId ? "Редактирование" : "Новый студент";
}
function hideForm() {
    document.getElementById("form-panel").style.display = "none";
    editingId = null;
    document.getElementById("last_name").value = "";
    document.getElementById("first_name").value = "";
    document.getElementById("email").value = "";
}
 
// Сохранить (создание или обновление)
async function saveStudent() {
    const data = {
        last_name: document.getElementById("last_name").value,
        first_name: document.getElementById("first_name").value,
        email: document.getElementById("email").value,
    };
    const url = editingId
        ? `${API}/students/${editingId}`
        : `${API}/students`;
    const method = editingId ? "PUT" : "POST";
 
    await fetch(url, {
        method, headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data),
    });
    hideForm();
    loadStudents();
}
 
// Редактирование
async function editStudent(id) {
    const resp = await fetch(`${API}/students/${id}`);
    const s = await resp.json();
    document.getElementById("last_name").value = s.last_name;
    document.getElementById("first_name").value = s.first_name;
    document.getElementById("email").value = s.email || "";
    editingId = id;
    showForm();
}
 
// Удаление
async function deleteStudent(id) {
    if (!confirm("Удалить студента?")) return;
    await fetch(`${API}/students/${id}`, { method: "DELETE" });
    loadStudents();
}
 
// Загрузка при старте
loadStudents();
