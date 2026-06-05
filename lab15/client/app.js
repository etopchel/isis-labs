const API = "http://localhost:5000/api";
let currentUser = null;
let currentProfile = null;
let editingId = null;
let selectedGroupId = null;

// ========== AUTH ==========

async function login() {
    const login_ = document.getElementById("login-login").value;
    const password = document.getElementById("login-password").value;
    const err = document.getElementById("login-error");

    const resp = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ login: login_, password }),
    });
    if (!resp.ok) {
        const data = await resp.json();
        err.textContent = data.error || "Ошибка входа";
        return;
    }
    err.textContent = "";
    const data = await resp.json();
    currentUser = data.user;
    currentProfile = data.profile;
    enterApp();
}

function showSignup() {
    document.getElementById("signup-form").style.display = "block";
}

function hideSignup() {
    document.getElementById("signup-form").style.display = "none";
}

async function signup() {
    const login_ = document.getElementById("signup-login").value;
    const password = document.getElementById("signup-password").value;
    const name = document.getElementById("signup-name").value;
    const userType = document.getElementById("signup-type").value;
    const err = document.getElementById("signup-error");

    const resp = await fetch(`${API}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ login: login_, password, user_type: userType, name }),
    });
    if (!resp.ok) {
        const data = await resp.json();
        err.textContent = data.error || "Ошибка регистрации";
        return;
    }
    err.textContent = "";
    const data = await resp.json();
    currentUser = data.user;
    currentProfile = data.profile;
    hideSignup();
    enterApp();
}

function logout() {
    currentUser = null;
    currentProfile = null;
    document.getElementById("auth-panel").style.display = "block";
    document.getElementById("teacher-panel").style.display = "none";
    document.getElementById("student-panel").style.display = "none";
    document.getElementById("user-info").style.display = "none";
    document.getElementById("login-login").value = "";
    document.getElementById("login-password").value = "";
}

function enterApp() {
    document.getElementById("auth-panel").style.display = "none";
    document.getElementById("user-info").style.display = "block";
    document.getElementById("user-label").textContent =
        `Вы вошли как: ${currentProfile.name} (${currentUser.user_type === "teacher" ? "Преподаватель" : "Студент"})`;

    if (currentUser.user_type === "teacher") {
        document.getElementById("teacher-panel").style.display = "block";
        document.getElementById("student-panel").style.display = "none";
        loadTeacherProfile();
        loadStyles();
        loadGroups();
        loadPrograms();
        loadLessons();
    } else {
        document.getElementById("student-panel").style.display = "block";
        document.getElementById("teacher-panel").style.display = "none";
        loadStudentProfile();
        loadMyGroups();
        loadMyLessons("future");
    }
}

// ========== TABS ==========

function showTeacherTab(tab) {
    const panels = ["profile", "styles", "groups", "programs", "lessons"];
    panels.forEach(p => {
        document.getElementById(`t-${p}`).style.display = p === tab ? "block" : "none";
    });
    document.querySelectorAll("#teacher-panel .tab-bar button").forEach(b => {
        b.classList.toggle("active", b.textContent.includes({
            profile: "Профиль", styles: "Стили", groups: "Группы",
            programs: "Программы", lessons: "Уроки"
        }[tab]));
    });
}

function showStudentTab(tab) {
    const panels = ["profile", "groups", "lessons"];
    panels.forEach(p => {
        document.getElementById(`s-${p}`).style.display = p === tab ? "block" : "none";
    });
    document.querySelectorAll("#student-panel .tab-bar button").forEach(b => {
        b.classList.toggle("active", b.textContent.includes({
            profile: "Профиль", groups: "Группы", lessons: "Уроки"
        }[tab]));
    });
}

// ========== TEACHER PROFILE ==========

function loadTeacherProfile() {
    document.getElementById("t-name").value = currentProfile.name || "";
    document.getElementById("t-phone").value = currentProfile.phone || "";
    document.getElementById("t-email").value = currentProfile.email || "";
    document.getElementById("t-sex").value = currentProfile.sex || "";
    document.getElementById("t-age").value = currentProfile.age || "";
}

async function saveTeacherProfile() {
    const data = {
        name: document.getElementById("t-name").value,
        phone: document.getElementById("t-phone").value,
        email: document.getElementById("t-email").value,
        sex: document.getElementById("t-sex").value,
        age: parseInt(document.getElementById("t-age").value) || null,
    };
    const resp = await fetch(`${API}/teachers/${currentProfile.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (resp.ok) {
        currentProfile = await resp.json();
        document.getElementById("user-label").textContent =
            `Вы вошли как: ${currentProfile.name} (Преподаватель)`;
    }
}

// ========== STUDENT PROFILE ==========

function loadStudentProfile() {
    document.getElementById("s-name").value = currentProfile.name || "";
    document.getElementById("s-phone").value = currentProfile.phone || "";
    document.getElementById("s-email").value = currentProfile.email || "";
    document.getElementById("s-sex").value = currentProfile.sex || "";
    document.getElementById("s-age").value = currentProfile.age || "";
}

async function saveStudentProfile() {
    const data = {
        name: document.getElementById("s-name").value,
        phone: document.getElementById("s-phone").value,
        email: document.getElementById("s-email").value,
        sex: document.getElementById("s-sex").value,
        age: parseInt(document.getElementById("s-age").value) || null,
    };
    const resp = await fetch(`${API}/students/${currentProfile.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (resp.ok) {
        currentProfile = await resp.json();
        document.getElementById("user-label").textContent =
            `Вы вошли как: ${currentProfile.name} (Студент)`;
    }
}

// ========== STYLES ==========

async function loadStyles() {
    const resp = await fetch(`${API}/styles`);
    const styles = await resp.json();
    const tbody = document.getElementById("styles-table");
    tbody.innerHTML = styles.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.name}</td>
            <td>
                <button class="btn btn-edit btn-sm" onclick='editStyle(${s.id},"${s.name}")'>Изм.</button>
                <button class="btn btn-delete btn-sm" onclick='deleteStyle(${s.id})'>Удал.</button>
            </td>
        </tr>
    `).join("");
}

let styleEditingId = null;

function showStyleForm() {
    document.getElementById("style-form").style.display = "block";
}

function hideStyleForm() {
    document.getElementById("style-form").style.display = "none";
    document.getElementById("style-name").value = "";
    styleEditingId = null;
}

function editStyle(id, name) {
    styleEditingId = id;
    document.getElementById("style-name").value = name;
    showStyleForm();
}

async function saveStyle() {
    const name = document.getElementById("style-name").value;
    if (!name) return;

    const url = styleEditingId ? `${API}/styles/${styleEditingId}` : `${API}/styles`;
    const method = styleEditingId ? "PUT" : "POST";

    await fetch(url, { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name }) });
    hideStyleForm();
    loadStyles();
    fillStyleSelects();
}

async function deleteStyle(id) {
    if (!confirm("Удалить стиль?")) return;
    await fetch(`${API}/styles/${id}`, { method: "DELETE" });
    loadStyles();
    fillStyleSelects();
}

// ========== GROUPS ==========

async function loadGroups() {
    const resp = await fetch(`${API}/groups`);
    const groups = await resp.json();
    const tbody = document.getElementById("groups-table");
    tbody.innerHTML = groups.map(g => `
        <tr>
            <td>${g.id}</td>
            <td>${g.name}</td>
            <td>${g.age_from || 0} - ${g.age_to || "∞"}</td>
            <td>${g.style_name || "---"}</td>
            <td>
                <button class="btn btn-edit btn-sm" onclick='editGroup(${JSON.stringify(g).replace(/"/g,"&quot;")})'>Изм.</button>
                <button class="btn btn-delete btn-sm" onclick='deleteGroup(${g.id})'>Удал.</button>
                <button class="btn btn-primary btn-sm" onclick='showGroupStudents(${g.id},"${g.name}")'>Студенты</button>
            </td>
        </tr>
    `).join("");
    fillGroupSelect();
}

let groupEditingId = null;

function showGroupForm() {
    document.getElementById("group-form").style.display = "block";
    fillStyleSelects();
}

function hideGroupForm() {
    document.getElementById("group-form").style.display = "none";
    document.getElementById("group-name").value = "";
    document.getElementById("group-age-from").value = "";
    document.getElementById("group-age-to").value = "";
    document.getElementById("group-style").value = "";
    groupEditingId = null;
}

function editGroup(g) {
    groupEditingId = g.id;
    document.getElementById("group-name").value = g.name;
    document.getElementById("group-age-from").value = g.age_from || "";
    document.getElementById("group-age-to").value = g.age_to || "";
    fillStyleSelects();
    setTimeout(() => document.getElementById("group-style").value = g.style_id, 100);
    showGroupForm();
}

async function saveGroup() {
    const data = {
        name: document.getElementById("group-name").value,
        age_from: parseInt(document.getElementById("group-age-from").value) || null,
        age_to: parseInt(document.getElementById("group-age-to").value) || null,
        style_id: parseInt(document.getElementById("group-style").value) || null,
    };
    if (!data.name) return;

    const url = groupEditingId ? `${API}/groups/${groupEditingId}` : `${API}/groups`;
    const method = groupEditingId ? "PUT" : "POST";
    await fetch(url, { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
    hideGroupForm();
    loadGroups();
    fillGroupSelect();
}

async function deleteGroup(id) {
    if (!confirm("Удалить группу?")) return;
    await fetch(`${API}/groups/${id}`, { method: "DELETE" });
    loadGroups();
    fillGroupSelect();
}

// ========== GROUP STUDENTS ==========

async function showGroupStudents(groupId, groupName) {
    selectedGroupId = groupId;
    document.getElementById("gs-group-name").textContent = groupName;
    document.getElementById("group-students").style.display = "block";

    const resp = await fetch(`${API}/groups/${groupId}/students`);
    const students = await resp.json();
    const tbody = document.getElementById("group-students-table");
    tbody.innerHTML = students.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.name}</td>
            <td>${s.email || "---"}</td>
            <td><button class="btn btn-delete btn-sm" onclick='removeStudentFromGroup(${s.id})'>Удал.</button></td>
        </tr>
    `).join("");

    fillStudentSelect();
}

async function hideGroupStudents() {
    document.getElementById("group-students").style.display = "none";
    selectedGroupId = null;
}

async function fillStudentSelect() {
    const select = document.getElementById("gs-student-select");
    const resp = await fetch(`${API}/students`);
    const students = await resp.json();
    select.innerHTML = '<option value="">-- Выберите студента --</option>' +
        students.map(s => `<option value="${s.id}">${s.name}</option>`).join("");
}

async function addStudentToGroup() {
    const select = document.getElementById("gs-student-select");
    let studentId = parseInt(select.value);
    if (!studentId) {
        // Try manual input
        studentId = parseInt(prompt("Введите ID студента:"));
    }
    if (!studentId || !selectedGroupId) return;

    const resp = await fetch(`${API}/groups/${selectedGroupId}/students`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: studentId }),
    });
    if (!resp.ok) {
        const data = await resp.json();
        alert(data.error || "Ошибка");
        return;
    }
    showGroupStudents(selectedGroupId, document.getElementById("gs-group-name").textContent);
}

async function removeStudentFromGroup(studentId) {
    if (!confirm("Удалить студента из группы?")) return;
    await fetch(`${API}/groups/${selectedGroupId}/students/${studentId}`, { method: "DELETE" });
    showGroupStudents(selectedGroupId, document.getElementById("gs-group-name").textContent);
}

// ========== PROGRAMS ==========

async function loadPrograms() {
    const resp = await fetch(`${API}/programs`);
    const programs = await resp.json();
    const tbody = document.getElementById("programs-table");
    tbody.innerHTML = programs.map(p => `
        <tr>
            <td>${p.id}</td>
            <td>${p.name}</td>
            <td>${p.style_name || "---"}</td>
            <td>${p.track || "---"}</td>
            <td>${p.duration || "---"}</td>
            <td>
                <button class="btn btn-edit btn-sm" onclick='editProgram(${JSON.stringify(p).replace(/"/g,"&quot;")})'>Изм.</button>
                <button class="btn btn-delete btn-sm" onclick='deleteProgram(${p.id})'>Удал.</button>
            </td>
        </tr>
    `).join("");
    fillProgramSelect();
}

let progEditingId = null;

function showProgramForm() {
    document.getElementById("program-form").style.display = "block";
    fillStyleSelects();
}

function hideProgramForm() {
    document.getElementById("program-form").style.display = "none";
    document.getElementById("prog-name").value = "";
    document.getElementById("prog-style").value = "";
    document.getElementById("prog-track").value = "";
    document.getElementById("prog-duration").value = "";
    progEditingId = null;
}

function editProgram(p) {
    progEditingId = p.id;
    document.getElementById("prog-name").value = p.name;
    fillStyleSelects();
    setTimeout(() => {
        document.getElementById("prog-style").value = p.style_id;
    }, 100);
    document.getElementById("prog-track").value = p.track || "";
    document.getElementById("prog-duration").value = p.duration || "";
    showProgramForm();
}

async function saveProgram() {
    const data = {
        name: document.getElementById("prog-name").value,
        style_id: parseInt(document.getElementById("prog-style").value) || null,
        track: document.getElementById("prog-track").value,
        duration: document.getElementById("prog-duration").value,
    };
    if (!data.name) return;

    const url = progEditingId ? `${API}/programs/${progEditingId}` : `${API}/programs`;
    const method = progEditingId ? "PUT" : "POST";
    await fetch(url, { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
    hideProgramForm();
    loadPrograms();
    fillProgramSelect();
}

async function deleteProgram(id) {
    if (!confirm("Удалить программу?")) return;
    await fetch(`${API}/programs/${id}`, { method: "DELETE" });
    loadPrograms();
    fillProgramSelect();
}

// ========== LESSONS ==========

async function loadLessons() {
    let url = `${API}/lessons`;
    const dateFilter = document.getElementById("lesson-date-filter").value;
    if (dateFilter) url += `?date=${dateFilter}`;

    const resp = await fetch(url);
    const lessons = await resp.json();
    const tbody = document.getElementById("lessons-table");
    tbody.innerHTML = lessons.map(l => {
        const start = l.datetime_start ? l.datetime_start.replace("T", " ").substring(0, 16) : "---";
        const end = l.datetime_end ? l.datetime_end.replace("T", " ").substring(0, 16) : "---";
        return `
        <tr>
            <td>${l.id}</td>
            <td>${l.group_name || "---"}</td>
            <td>${l.program_name || "---"}</td>
            <td>${start}</td>
            <td>${end}</td>
            <td>
                <button class="btn btn-edit btn-sm" onclick='editLesson(${l.id})'>Изм.</button>
                <button class="btn btn-delete btn-sm" onclick='deleteLesson(${l.id})'>Удал.</button>
            </td>
        </tr>`;
    }).join("");
}

function clearLessonFilter() {
    document.getElementById("lesson-date-filter").value = "";
    loadLessons();
}

let lessonEditingId = null;

function showLessonForm() {
    document.getElementById("lesson-form").style.display = "block";
    fillGroupSelect();
    fillProgramSelect();
}

function hideLessonForm() {
    document.getElementById("lesson-form").style.display = "none";
    document.getElementById("lesson-group").value = "";
    document.getElementById("lesson-program").value = "";
    document.getElementById("lesson-start").value = "";
    document.getElementById("lesson-end").value = "";
    lessonEditingId = null;
}

async function editLesson(id) {
    lessonEditingId = id;
    // Fetch the lesson data
    const resp = await fetch(`${API}/lessons`);
    const lessons = await resp.json();
    const lesson = lessons.find(l => l.id === id);
    if (!lesson) return;

    fillGroupSelect();
    fillProgramSelect();
    setTimeout(() => {
        document.getElementById("lesson-group").value = lesson.group_id;
        document.getElementById("lesson-program").value = lesson.program_id;
    }, 100);
    if (lesson.datetime_start) {
        document.getElementById("lesson-start").value = lesson.datetime_start.substring(0, 16);
    }
    if (lesson.datetime_end) {
        document.getElementById("lesson-end").value = lesson.datetime_end.substring(0, 16);
    }
    showLessonForm();
}

async function saveLesson() {
    const startVal = document.getElementById("lesson-start").value;
    const endVal = document.getElementById("lesson-end").value;
    const data = {
        group_id: parseInt(document.getElementById("lesson-group").value) || null,
        program_id: parseInt(document.getElementById("lesson-program").value) || null,
        datetime_start: startVal ? startVal.replace("T", " ") + ":00" : null,
        datetime_end: endVal ? endVal.replace("T", " ") + ":00" : null,
    };
    if (!data.group_id || !data.program_id || !data.datetime_start || !data.datetime_end) return;

    const url = lessonEditingId ? `${API}/lessons/${lessonEditingId}` : `${API}/lessons`;
    const method = lessonEditingId ? "PUT" : "POST";
    await fetch(url, { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
    hideLessonForm();
    loadLessons();
}

async function deleteLesson(id) {
    if (!confirm("Удалить урок?")) return;
    await fetch(`${API}/lessons/${id}`, { method: "DELETE" });
    loadLessons();
}

// ========== STUDENT: MY GROUPS & LESSONS ==========

async function loadMyGroups() {
    const resp = await fetch(`${API}/me/groups?user_id=${currentUser.id}`);
    const groups = await resp.json();
    const tbody = document.getElementById("my-groups-table");
    tbody.innerHTML = groups.map(g => {
        const ageRange = `${g.age_from || 0} - ${g.age_to || "∞"}`;
        return `
        <tr>
            <td>${g.id}</td>
            <td>${g.name}</td>
            <td>${g.style_name || "---"}</td>
            <td>${ageRange}</td>
        </tr>`;
    }).join("");
}

async function loadMyLessons(period) {
    let url = `${API}/me/lessons?user_id=${currentUser.id}`;
    if (period && period !== "all") url += `&period=${period}`;

    const resp = await fetch(url);
    const lessons = await resp.json();
    const tbody = document.getElementById("my-lessons-table");
    tbody.innerHTML = lessons.map(l => {
        const start = l.datetime_start ? l.datetime_start.replace("T", " ").substring(0, 16) : "---";
        const end = l.datetime_end ? l.datetime_end.replace("T", " ").substring(0, 16) : "---";
        return `
        <tr>
            <td>${l.id}</td>
            <td>${l.group_name || "---"}</td>
            <td>${l.program_name || "---"}</td>
            <td>${start}</td>
            <td>${end}</td>
        </tr>`;
    }).join("");
}

// ========== COMMON HELPERS ==========

async function fillStyleSelects() {
    const resp = await fetch(`${API}/styles`);
    const styles = await resp.json();
    ["group-style", "prog-style"].forEach(id => {
        const select = document.getElementById(id);
        const val = select.value;
        select.innerHTML = '<option value="">-- Выберите --</option>' +
            styles.map(s => `<option value="${s.id}">${s.name}</option>`).join("");
        select.value = val;
    });
}

async function fillGroupSelect() {
    const resp = await fetch(`${API}/groups`);
    const groups = await resp.json();
    const select = document.getElementById("lesson-group");
    const val = select.value;
    select.innerHTML = '<option value="">-- Выберите --</option>' +
        groups.map(g => `<option value="${g.id}">${g.name}</option>`).join("");
    select.value = val;
}

async function fillProgramSelect() {
    const resp = await fetch(`${API}/programs`);
    const programs = await resp.json();
    const select = document.getElementById("lesson-program");
    const val = select.value;
    select.innerHTML = '<option value="">-- Выберите --</option>' +
        programs.map(p => `<option value="${p.id}">${p.name}</option>`).join("");
    select.value = val;
}
