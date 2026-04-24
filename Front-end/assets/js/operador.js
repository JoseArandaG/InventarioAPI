// Front-end/assets/js/operator.js

async function registrarMovimiento(tipo) {
    const id_prod = prompt("Ingrese ID del Producto:");
    const cantidad = prompt("Cantidad:");
    const token = localStorage.getItem('token');

    if(!id_prod || !cantidad) return;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/movimientos/registrar/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                id_producto: id_prod,
                cantidad: cantidad,
                tipo_movimiento: tipo
            })
        });

        if(response.ok) {
            alert("Movimiento registrado con éxito");
            location.reload();
        }
    } catch (e) {
        alert("Error al conectar con la API");
    }
}

async function cargarHistorial() {
    const container = document.getElementById('historial-movimientos');
    const user = JSON.parse(localStorage.getItem('user'));
    if(!user || !container) return;
    
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/movimientos/usuario/${user.id_usuario}/`);
        const datos = await response.json();
        container.innerHTML = datos.map(mov => `
            <div class="flex items-center justify-between p-4 bg-slate-50 rounded-2xl">
                <div>
                    <p class="text-sm font-bold">${mov.producto_nombre}</p>
                    <p class="text-[10px] text-slate-400">${mov.fecha}</p>
                </div>
                <span class="font-bold ${mov.tipo === 'entrada' ? 'text-green-600' : 'text-red-600'}">
                    ${mov.tipo === 'entrada' ? '+' : '-'}${mov.cantidad}
                </span>
            </div>`).join('');
    } catch (e) {
        container.innerHTML = '<p class="text-slate-400 text-center">No hay movimientos recientes.</p>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    verificarSesion();
    cargarHistorial();
});