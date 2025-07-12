// JavaScript para el Controlador de Carrera
let raceStatus = {
    current_laps: 0,
    max_laps: 15,
    remaining_laps: 15,
    is_completed: false,
    progress_percentage: 0
};
let ledStatus = false;
let connectionStatus = 'connecting';

// Función para actualizar la interfaz
function updateUI() {
    const currentLapElement = document.getElementById('currentLap');
    const maxLapsElement = document.getElementById('maxLaps');
    const progressFillElement = document.getElementById('progressFill');
    const raceStatusElement = document.getElementById('raceStatus');
    const connectionStatusElement = document.getElementById('connectionStatus');
    
    // Actualizar contador de vueltas
    currentLapElement.textContent = raceStatus.current_laps;
    maxLapsElement.textContent = raceStatus.max_laps;
    
    // Actualizar barra de progreso
    progressFillElement.style.width = `${raceStatus.progress_percentage}%`;
    
    // Actualizar estado de la carrera
    if (raceStatus.is_completed) {
        raceStatusElement.textContent = '¡Carrera completada!';
        raceStatusElement.style.color = '#4CAF50';
    } else if (raceStatus.current_laps === 0) {
        raceStatusElement.textContent = 'Listo para comenzar';
        raceStatusElement.style.color = '#666';
    } else {
        raceStatusElement.textContent = `Vuelta ${raceStatus.current_laps} de ${raceStatus.max_laps}`;
        raceStatusElement.style.color = '#333';
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

// Función para incrementar vuelta
async function incrementLap() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Incrementando...';
    }
    
    try {
        const response = await fetch('/api/lap/increment');
        const data = await response.json();
        
        if (data.success) {
            raceStatus = data.race_status;
            showNotification('Vuelta incrementada', 'success');
        } else {
            showNotification(data.message, 'warning');
        }
        
        updateUI();
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al incrementar vuelta', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">🏁</span>Incrementar Vuelta';
    }
}

// Función para reiniciar carrera
async function resetRace() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Reiniciando...';
    }
    
    try {
        const response = await fetch('/api/lap/reset');
        const data = await response.json();
        
        if (data.success) {
            raceStatus = data.race_status;
            showNotification('Carrera reiniciada', 'success');
        }
        
        updateUI();
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al reiniciar carrera', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">🔄</span>Reiniciar Carrera';
    }
}

// Función para alternar LED
async function toggleLED() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Alternando...';
    }
    
    await apiCall('/api/led/toggle');
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">🔴</span>Alternar LED';
    }
}

// Función para encender el LED
async function turnOnLED() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Encendiendo...';
    }
    await apiCall('/api/led/on');
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">🔴</span>Encender LED';
    }
}

// Función para apagar el LED
async function turnOffLED() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Apagando...';
    }
    await apiCall('/api/led/off');
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">⚪</span>Apagar LED';
    }
}

// Función para obtener el estado actual
async function getStatus() {
    try {
        const response = await fetch('/api/lap/status');
        const data = await response.json();
        
        if (data.success) {
            raceStatus = data.race_status;
            ledStatus = data.race_status.led_status.is_on;
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

// Función para obtener nombre del piloto
async function getRacerName() {
    try {
        const response = await fetch('/api/racer/name');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('currentRacerName').textContent = data.racer_name;
            document.getElementById('racerName').value = data.racer_name;
        }
    } catch (error) {
        console.error('Error obteniendo nombre del piloto:', error);
    }
}

// Función para establecer nombre del piloto
async function setRacerName() {
    const racerName = document.getElementById('racerName').value.trim().toUpperCase();
    
    if (!racerName) {
        showNotification('Por favor ingresa un nombre', 'warning');
        return;
    }
    
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Guardando...';
    }
    
    try {
        // Llamar a la API para cambiar el nombre del piloto
        const response = await fetch(`/api/racer/name/set?name=${encodeURIComponent(racerName)}`);
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('currentRacerName').textContent = data.racer_name;
            document.getElementById('racerName').value = racerName; // Mantener mayúsculas en el campo
            showNotification('Nombre del piloto actualizado y mostrado en display', 'success');
        } else {
            showNotification(data.message || 'Error al actualizar nombre', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al actualizar nombre', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">💾</span>Guardar Nombre';
    }
}

// Función para mostrar nombre del piloto en display
async function displayRacerName() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Mostrando...';
    }
    
    try {
        const response = await fetch('/api/racer/display');
        const data = await response.json();
        
        if (data.success) {
            showNotification('Nombre mostrado en display', 'success');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al mostrar nombre', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">📺</span>Mostrar en Display';
    }
}

// Función para convertir a mayúsculas mientras se escribe
function convertToUpperCase(input) {
    input.value = input.value.toUpperCase();
}

// Inicializar la página
document.addEventListener('DOMContentLoaded', function() {
    updateDeviceIP();
    
    // Obtener estado inicial
    getStatus();
    
    // Obtener nombre del piloto
    getRacerName();
    
    // Configurar conversión automática a mayúsculas
    const racerNameInput = document.getElementById('racerName');
    if (racerNameInput) {
        racerNameInput.addEventListener('input', function() {
            convertToUpperCase(this);
        });
    }
    
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