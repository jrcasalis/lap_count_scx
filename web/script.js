// JavaScript para el Controlador LED
let ledStatus = false;
let connectionStatus = 'connecting';

// Función para actualizar la interfaz
function updateUI() {
    const ledLight = document.getElementById('ledLight');
    const statusText = document.getElementById('statusText');
    const connectionStatusElement = document.getElementById('connectionStatus');
    
    // Actualizar LED
    if (ledStatus) {
        ledLight.classList.add('on');
        statusText.textContent = 'Estado: Encendido';
    } else {
        ledLight.classList.remove('on');
        statusText.textContent = 'Estado: Apagado';
    }
    
    // Actualizar estado de conexión
    connectionStatusElement.textContent = getConnectionStatusText();
    connectionStatusElement.className = `connection-status ${connectionStatus}`;
}

// Función para obtener texto del estado de conexión
function getConnectionStatusText() {
    switch(connectionStatus) {
        case 'connected':
            return 'Conectado';
        case 'disconnected':
            return 'Desconectado';
        case 'connecting':
            return 'Conectando...';
        default:
            return 'Desconocido';
    }
}

// Función para hacer peticiones a la API
async function apiCall(endpoint) {
    try {
        connectionStatus = 'connecting';
        updateUI();
        
        const response = await fetch(endpoint);
        const data = await response.json();
        
        if (data.success) {
            ledStatus = data.is_on;
            connectionStatus = 'connected';
            updateUI();
            return data;
        } else {
            console.error('Error:', data.message);
            connectionStatus = 'disconnected';
            updateUI();
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        connectionStatus = 'disconnected';
        updateUI();
    }
}

// Función para encender el LED
async function turnOn() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Encendiendo...';
    }
    
    await apiCall('/api/led/on');
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">🔴</span>Encender';
    }
}

// Función para apagar el LED
async function turnOff() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Apagando...';
    }
    
    await apiCall('/api/led/off');
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">⚫</span>Apagar';
    }
}

// Función para alternar el LED
async function toggle() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Alternando...';
    }
    
    await apiCall('/api/led/toggle');
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">🔄</span>Alternar';
    }
}

// Función para obtener el estado actual
async function getStatus() {
    try {
        const response = await fetch('/api/led/status');
        const data = await response.json();
        
        if (data.success) {
            ledStatus = data.is_on;
            connectionStatus = 'connected';
            updateUI();
        }
    } catch (error) {
        console.error('Error obteniendo estado:', error);
        connectionStatus = 'disconnected';
        updateUI();
    }
}

// Actualizar IP del dispositivo
function updateDeviceIP() {
    const deviceIP = document.getElementById('deviceIP');
    deviceIP.textContent = window.location.hostname;
}

// Función para verificar conectividad
async function checkConnectivity() {
    try {
        const response = await fetch('/api/led/status', { 
            method: 'HEAD',
            timeout: 3000 
        });
        connectionStatus = 'connected';
    } catch (error) {
        connectionStatus = 'disconnected';
    }
    updateUI();
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Estilos básicos
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    // Colores según tipo
    switch(type) {
        case 'success':
            notification.style.backgroundColor = '#4CAF50';
            break;
        case 'error':
            notification.style.backgroundColor = '#f44336';
            break;
        case 'warning':
            notification.style.backgroundColor = '#ff9800';
            break;
        default:
            notification.style.backgroundColor = '#2196F3';
    }
    
    document.body.appendChild(notification);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Agregar estilos CSS para animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Inicializar la página
document.addEventListener('DOMContentLoaded', function() {
    updateDeviceIP();
    
    // Obtener estado inicial
    getStatus();
    
    // Verificar conectividad cada 10 segundos
    setInterval(checkConnectivity, 10000);
    
    // Actualizar estado cada 5 segundos
    setInterval(getStatus, 5000);
    
    // Mostrar notificación de bienvenida
    setTimeout(() => {
        showNotification('Controlador LED iniciado correctamente', 'success');
    }, 1000);
});

// Manejar errores de red
window.addEventListener('online', function() {
    showNotification('Conexión restaurada', 'success');
    checkConnectivity();
});

window.addEventListener('offline', function() {
    showNotification('Conexión perdida', 'error');
    connectionStatus = 'disconnected';
    updateUI();
}); 