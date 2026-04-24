// Front-end/assets/js/admin.js

async function cargarProductos() {
    const token = localStorage.getItem('token');
    const tabla = document.getElementById('tabla-productos');
    
    if (!tabla) return;
    tabla.innerHTML = '<tr><td colspan="4" class="p-10 text-center text-slate-400">Cargando productos...</td></tr>';

    try {
        const response = await fetch('http://127.0.0.1:8000/api/productos/listar/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const productos = await response.json();
        
        tabla.innerHTML = ''; 
        productos.forEach(prod => {
            const colorEstado = prod.stock > 10 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700';
            tabla.innerHTML += `
                <tr class="hover:bg-slate-50">
                    <td class="px-6 py-4 font-bold text-slate-800">${prod.nombre_producto}</td>
                    <td class="px-6 py-4 text-slate-500">${prod.categoria}</td>
                    <td class="px-6 py-4 font-mono font-bold">${prod.stock}</td>
                    <td class="px-6 py-4">
                        <span class="px-2 py-1 rounded-full text-[10px] font-bold uppercase ${colorEstado}">
                            ${prod.stock > 10 ? 'Óptimo' : 'Crítico'}
                        </span>
                    </td>
                </tr>`;
        });
    } catch (e) {
        tabla.innerHTML = '<tr><td colspan="4" class="p-10 text-center text-red-500">Error de conexión con la API.</td></tr>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    verificarSesion(); 
    const user = JSON.parse(localStorage.getItem('user'));
    if(user && document.getElementById('user-name')) {
        document.getElementById('user-name').innerText = `${user.nombre} (Admin)`;
    }
    cargarProductos();
});