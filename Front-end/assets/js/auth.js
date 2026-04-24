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

    // 1. Resetear estado: ocultar error anterior y mostrar carga
    mensajeError.classList.add('hidden');
    mensajeError.innerText = ''; // Limpiamos el texto previo
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
            // ... (Tu lógica de guardado de token se mantiene igual)
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));

            const rol = data.user.rol.toLowerCase();
            window.location.href = (rol === 'operador') ? '/operator-dashboard/' : '/admin-dashboard/';
        } else {
            // 2. Manejo de error específico de la API
            // Si tu API de Django usa "detail" o "error", asegúrate de capturarlo:
            mensajeError.innerText = data.error || data.detail || 'Usuario o contraseña incorrectos';
            mensajeError.classList.remove('hidden');
        }
    } catch (error) {
        // 3. Manejo de error de red o servidor caído
        console.error("Error de login:", error);
        mensajeError.innerText = 'No se pudo conectar con el servidor. Inténtalo más tarde.';
        mensajeError.classList.remove('hidden');
    } finally {
        // 4. Restaurar botón y ocultar loader
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