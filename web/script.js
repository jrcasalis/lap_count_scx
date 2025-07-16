// Script para Control Carrera Pico W
// Utilidad para mostrar mensajes en el div #msg
function mostrarMensaje(texto, tipo) {
    var msg = document.getElementById('msg');
    msg.textContent = texto;
    msg.className = 'msg ' + (tipo || '');
}

// Test simple: solo feedback local
function testSimple() {
    console.log('Test simple ejecutado');
    mostrarMensaje('✅ Test simple funcionando', 'success');
}

// Test de conexión: fetch a /
function testFetch() {
    console.log('Test fetch ejecutado');
    mostrarMensaje('Probando conexión...', 'loading');
    fetch('/')
        .then(function(response) {
            console.log('Respuesta fetch:', response.status);
            mostrarMensaje('✅ Conexión exitosa', 'success');
        })
        .catch(function(error) {
            console.error('Error fetch:', error);
            mostrarMensaje('❌ Error de conexión: ' + error.message, 'error');
        });
}

// Función para acciones de carrera
function accion(ruta) {
    console.log('Ejecutando acción:', ruta);
    mostrarMensaje('Enviando comando...', 'loading');
    fetch(ruta)
        .then(function(response) {
            console.log('Respuesta HTTP:', response.status);
            return response.json();
        })
        .then(function(data) {
            console.log('Respuesta JSON:', data);
            if (data.success) {
                mostrarMensaje('✅ ' + data.message, 'success');
            } else {
                mostrarMensaje('❌ Error: ' + data.message, 'error');
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
            mostrarMensaje('❌ Error: ' + error.message, 'error');
        });
}

// Inicialización al cargar la página
window.onload = function() {
    console.log('Interfaz web inicializada');
    mostrarMensaje('Interfaz lista para usar', '');
};

// Exponer funciones globalmente para los onclick del HTML
window.testSimple = testSimple;
window.testFetch = testFetch;
window.accion = accion;

//console.log('script.js cargado y funciones globales listas'); 