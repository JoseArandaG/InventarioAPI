const API_BASE_URL = "http://127.0.0.1:8000/api";

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
});

async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const mensajeError = document.getElementById('mensaje-error');
    const btnSubmit = document.getElementById('btnSubmit');
    const loader = document.getElementById('loader');

    // Estado de carga
    mensajeError.classList.add('hidden');
    loader.classList.remove('hidden');
    btnSubmit.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Guardar sesión
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));

            const rol = data.user.rol.toLowerCase();
            if (rol === 'operador') {
            window.location.href = '/operator-dashboard/'; // Coincide con tu urls.py
            } else {
             window.location.href = '/admin-dashboard/';    // Coincide con tu urls.py
    }
        } else {
            mensajeError.innerText = data.error || 'Acceso denegado';
            mensajeError.classList.remove('hidden');
        }
    } catch (error) {
        mensajeError.innerText = 'Error de conexión con el servidor.';
        mensajeError.classList.remove('hidden');
    } finally {
        loader.classList.add('hidden');
        btnSubmit.disabled = false;
    }
}

function logout() {
    localStorage.clear();
    window.location.href = 'login.html';
}

// Agrega esto al final de assets/js/auth.js o en un script dentro del dashboard
function verificarSesion() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        window.location.href = 'login.html';
    }
    // Opcional: Mostrar nombre en el header
    const nameLabel = document.getElementById('user-name-display');
    if (nameLabel) nameLabel.innerText = user.nombre;
}

function logout() {
    // Borra el token y los datos del usuario del navegador
    localStorage.clear(); 
    
    // Redirige a la URL de login de Django
    window.location.href = '/login/'; 
}

function verificarSesion() {
    const token = localStorage.getItem('token');
    
    // Si no hay token, significa que no está logueado o cerró sesión
    if (!token) {
        window.location.href = '/login/';
    }
}