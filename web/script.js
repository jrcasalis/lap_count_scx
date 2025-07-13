// JavaScript para el Controlador de Carrera - Diseño de Cards
let raceStatus = {
    current_laps: 0,
    max_laps: 15,
    remaining_laps: 15,
    is_completed: false,
    progress_percentage: 0
};
let ledStatus = false;
let connectionStatus = 'connecting';

// Variable para el estado del semáforo
let trafficLightStatus = {
    state: 'off',
    red_on: false,
    yellow_on: false,
    green_on: false,
    blinking_active: false
};

// Función para actualizar la interfaz
function updateUI() {
    const currentLapElement = document.getElementById('currentLap');
    const maxLapsElement = document.getElementById('maxLaps');
    const progressFillElement = document.getElementById('progressFill');
    const raceStatusElement = document.getElementById('raceStatus');
    const connectionStatusElement = document.getElementById('connectionStatus');
    const ledIndicatorElement = document.getElementById('ledIndicator');
    const ledStatusElement = document.getElementById('ledStatus');
    const raceStateElement = document.getElementById('raceState');
    const lapCountElement = document.getElementById('lapCount');
    const raceInitStatusElement = document.getElementById('raceInitStatus');
    
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
    
    // Actualizar LED indicator
    if (ledIndicatorElement) {
        if (ledStatus) {
            ledIndicatorElement.classList.add('on');
            ledStatusElement.textContent = 'Encendido';
        } else {
            ledIndicatorElement.classList.remove('on');
            ledStatusElement.textContent = 'Apagado';
        }
    }
    
    // Actualizar estado de la carrera (nuevo) - SINCRONIZACIÓN REALTIME
    if (raceStateElement) {
        if (raceStatus.is_race_started) {
            raceStateElement.textContent = 'Iniciada';
            raceStateElement.style.color = '#28a745';
        } else {
            raceStateElement.textContent = 'No Iniciada';
            raceStateElement.style.color = '#dc3545';
        }
    }
    
    // Actualizar contador de vueltas (nuevo) - SINCRONIZACIÓN REALTIME
    if (lapCountElement) {
        lapCountElement.textContent = raceStatus.current_laps;
    }
    
    // Actualizar estado de inicialización de carrera (nuevo) - SINCRONIZACIÓN REALTIME
    if (raceInitStatusElement) {
        if (raceStatus.is_race_started) {
            raceInitStatusElement.textContent = 'Iniciada';
            raceInitStatusElement.style.color = '#28a745';
        } else {
            raceInitStatusElement.textContent = 'No Iniciada';
            raceInitStatusElement.style.color = '#dc3545';
        }
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
        button.innerHTML = '<span class="icon">🔄</span>Reiniciar';
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
        button.innerHTML = '<span class="icon">🔴</span>Encender';
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
        button.innerHTML = '<span class="icon">⚪</span>Apagar';
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

// Función para actualizar estado (nueva función para el botón de actualizar)
async function refreshStatus() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Actualizando...';
    }
    
    await getStatus();
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">🔄</span>Actualizar';
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
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    // Colores según tipo
    switch(type) {
        case 'success':
            notification.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
            break;
        case 'error':
            notification.style.background = 'linear-gradient(135deg, #dc3545, #e83e8c)';
            break;
        case 'warning':
            notification.style.background = 'linear-gradient(135deg, #ffc107, #fd7e14)';
            notification.style.color = '#333';
            break;
        default:
            notification.style.background = 'linear-gradient(135deg, #17a2b8, #20c997)';
    }
    
    // Agregar al DOM
    document.body.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// =============================================================================
// FUNCIONES DEL SEMÁFORO OPTIMIZADAS PARA SINCRONIZACIÓN ULTRA-RÁPIDA
// =============================================================================

// Función para actualizar la UI del semáforo con sincronización ultra-rápida
function updateTrafficLightUI() {
    const trafficLightStatusElement = document.getElementById('trafficLightStatus');
    const trafficLightsStateElement = document.getElementById('trafficLightsState');
    
    // Actualizar estado general del semáforo
    if (trafficLightStatusElement) {
        trafficLightStatusElement.textContent = trafficLightStatus.state;
        trafficLightStatusElement.className = `status-value ${trafficLightStatus.state}`;
    }
    
    // Actualizar estado detallado de las luces
    if (trafficLightsStateElement) {
        const redState = trafficLightStatus.red_on ? 'ON' : 'OFF';
        const yellowState = trafficLightStatus.yellow_on ? 'ON' : 'OFF';
        const greenState = trafficLightStatus.green_on ? 'ON' : 'OFF';
        
        trafficLightsStateElement.textContent = `Roja: ${redState} | Amarilla: ${yellowState} | Verde: ${greenState}`;
    }
    
    // Actualizar todos los semáforos (4 semáforos) - ULTRA-RÁPIDO
    updateAllTrafficLights();
}

// Función para actualizar todos los semáforos - OPTIMIZADA PARA VELOCIDAD
function updateAllTrafficLights() {
    const lightIds = ['1', '2', '3', '4'];
    
    lightIds.forEach(id => {
        // Actualizar luz roja
        const redLight = document.getElementById(`redLight${id}`);
        if (redLight) {
            if (trafficLightStatus.red_on) {
                redLight.classList.add('on');
            } else {
                redLight.classList.remove('on');
            }
        }
        
        // Actualizar luz amarilla
        const yellowLight = document.getElementById(`yellowLight${id}`);
        if (yellowLight) {
            if (trafficLightStatus.yellow_on) {
                yellowLight.classList.add('on');
            } else {
                yellowLight.classList.remove('on');
            }
        }
        
        // Actualizar luz verde - CRÍTICO PARA INICIO DE CARRERA
        const greenLight = document.getElementById(`greenLight${id}`);
        if (greenLight) {
            if (trafficLightStatus.green_on) {
                greenLight.classList.add('on');
            } else {
                greenLight.classList.remove('on');
            }
        }
    });
}

// Función para iniciar previa
async function startRacePrevious() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Iniciando...';
    }
    
    try {
        console.log('⚠️ Iniciando previa...');
        
        const response = await fetch('/api/traffic-light/previous');
        const data = await response.json();
        
        if (data.success) {
            console.log('✅ Previa iniciada correctamente');
            console.log('   Estado del semáforo:', data.traffic_light_status.state);
            
            showNotification('Previa iniciada', 'success');
            
            // Actualizar estado inmediatamente
            if (data.traffic_light_status) {
                trafficLightStatus = data.traffic_light_status;
                updateTrafficLightUI();
            }
            
            // Mostrar botón de terminar previa
            const stopPreviousBtn = document.getElementById('stopPreviousBtn');
            if (stopPreviousBtn) {
                stopPreviousBtn.style.display = 'inline-flex';
            }
        } else {
            console.error('❌ Error iniciando previa:', data.message);
            showNotification(data.message, 'warning');
        }
    } catch (error) {
        console.error('❌ Error de conexión:', error);
        showNotification('Error al iniciar previa', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">⚠️</span>Iniciar Previa';
    }
}

// Función para terminar previa (nueva)
async function stopRacePrevious() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Terminando...';
    }
    
    try {
        const response = await fetch('/api/traffic-light/previous-stop');
        const data = await response.json();
        
        if (data.success) {
            showNotification('Previa terminada', 'success');
            // Ocultar botón de terminar previa
            const stopPreviousBtn = document.getElementById('stopPreviousBtn');
            if (stopPreviousBtn) {
                stopPreviousBtn.style.display = 'none';
            }
        } else {
            showNotification(data.message, 'warning');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al terminar previa', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">⏹️</span>Terminar Previa';
    }
}

// Función para iniciar carrera
async function startRace() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Iniciando...';
    }
    
    try {
        console.log('🚦 Iniciando carrera...');
        
        const response = await fetch('/api/traffic-light/start');
        const data = await response.json();
        
        if (data.success) {
            console.log('✅ Carrera iniciada correctamente');
            console.log('   Estado del semáforo:', data.traffic_light_status.state);
            console.log('   Estado de la carrera:', data.race_status.is_race_started);
            
            showNotification('Carrera iniciada', 'success');
            
            // Actualizar estado inmediatamente
            if (data.traffic_light_status) {
                trafficLightStatus = data.traffic_light_status;
                updateTrafficLightUI();
            }
            
            if (data.race_status) {
                raceStatus = data.race_status;
                updateUI();
            }
        } else {
            console.error('❌ Error iniciando carrera:', data.message);
            showNotification(data.message, 'warning');
        }
    } catch (error) {
        console.error('❌ Error de conexión:', error);
        showNotification('Error al iniciar carrera', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">🏁</span>Largar';
    }
}

// Función para parar carrera
async function stopRace() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Parando...';
    }
    
    try {
        const response = await fetch('/api/traffic-light/stop');
        const data = await response.json();
        
        if (data.success) {
            showNotification('Carrera parada', 'success');
        } else {
            showNotification(data.message, 'warning');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al parar carrera', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">🛑</span>Parar';
    }
}

// Función para obtener estado del semáforo - ULTRA-OPTIMIZADA
async function getTrafficLightStatus() {
    try {
        const response = await fetch('/api/traffic-light/status', {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache'
            }
        });
        const data = await response.json();
        
        if (data.success) {
            // Solo actualizar si el estado realmente cambió
            const oldState = JSON.stringify(trafficLightStatus);
            trafficLightStatus = data.traffic_light_status;
            const newState = JSON.stringify(trafficLightStatus);
            
            if (oldState !== newState) {
                updateTrafficLightUI();
                // Log solo en debug
                if (DEBUG_ENABLED) {
                    console.log('🔄 Estado del semáforo actualizado:', trafficLightStatus.state);
                }
            }
        }
    } catch (error) {
        // Solo log en debug para no saturar consola
        if (DEBUG_ENABLED) {
            console.error('Error obteniendo estado del semáforo:', error);
        }
    }
}

// Función para sincronización ultra-rápida del semáforo visual
function syncTrafficLightVisual() {
    updateTrafficLightUI();
}

// =============================================================================
// FUNCIONES DEL PILOTO
// =============================================================================

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
    const racerNameInput = document.getElementById('racerName');
    const racerName = racerNameInput.value.trim();
    
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
        const response = await fetch(`/api/racer/name/set?name=${encodeURIComponent(racerName)}`);
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('currentRacerName').textContent = racerName;
            showNotification('Nombre guardado', 'success');
        } else {
            showNotification(data.message, 'warning');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al guardar nombre', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">💾</span>Guardar';
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
        } else {
            showNotification(data.message, 'warning');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al mostrar nombre', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">📺</span>Mostrar';
    }
}

// Función para convertir a mayúsculas
function convertToUpperCase(input) {
    input.value = input.value.toUpperCase();
}

// =============================================================================
// INICIALIZACIÓN Y ACTUALIZACIÓN CONTINUA ULTRA-OPTIMIZADA
// =============================================================================

// Cache para evitar actualizaciones innecesarias
let lastRaceStatus = null;
let lastTrafficStatus = null;
let updateCounter = 0;

// Función para actualizar datos en tiempo real - ULTRA-OPTIMIZADA
async function updateRealtimeData() {
    try {
        // Actualizar solo si es necesario (cada 3 ciclos)
        if (updateCounter % 3 === 0) {
            await getStatus();
        }
        
        // Actualizar semáforo más frecuentemente
        await getTrafficLightStatus();
        updateUI();
        
        updateCounter++;
    } catch (error) {
        console.error('❌ Error en actualización:', error);
    }
}

// Función de inicialización - ULTRA-OPTIMIZADA PARA VELOCIDAD MÁXIMA
async function initializeApp() {
    console.log('🚀 Iniciando aplicación ultra-optimizada...');
    
    updateDeviceIP();
    
    // Cargar datos iniciales
    await updateRealtimeData();
    
    // ACTUALIZACIÓN ULTRA-RÁPIDA: 200ms para máxima velocidad
    setInterval(updateRealtimeData, 200);
    
    // Sincronización ultra-rápida del semáforo cada 80ms
    setInterval(getTrafficLightStatus, 80);
    
    // Sincronización visual ultra-rápida cada 40ms
    setInterval(syncTrafficLightVisual, 40);
    
    // Verificar conectividad cada 3 segundos
    setInterval(checkConnectivity, 3000);
    
    console.log('⚡ Aplicación ultra-optimizada inicializada');
    console.log('🚀 Actualización: 200ms | Semáforos: 80ms | Visual: 40ms');
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initializeApp); 