const ESP32_URL = "http://192.168.100.47"; // Cambia esto por la IP de tu ESP32

// Función para manejar el encendido y apagado de focos
function handleSwitch(event) {
    const focoId = event.target.getAttribute("attr-focoId");
    const action = event.target.value.toLowerCase(); // "encender" o "apagar"

    fetch(`${ESP32_URL}/${action}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `foco=foco${focoId}`,
    })
        .then((response) => {
            if (response.ok) {
                // alert(`Foco ${focoId} ${action === "encender" ? "encendido" : "apagado"} correctamente.`);
            } else {
                // alert(`Error al intentar ${action} el foco ${focoId}.`);
            }
        })
        .catch((error) => {
            console.error(`Error al enviar la solicitud para el foco ${focoId}:`, error);
            // alert(`No se pudo ${action} el foco ${focoId}.`);
        });
}

// Función para manejar el cambio de luminosidad
function handleLuminosity(event) {
    const focoId = event.target.getAttribute("attr-focoId");
    const luminosity = event.target.value;

    fetch(`${ESP32_URL}/luminosidad`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `foco=foco${focoId}&valor=${luminosity}`,
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Error en la respuesta: ${response.statusText}`);
            }
            return response.text(); // Puedes procesar el texto o JSON si es necesario
        })
        .then((data) => {
            // alert(`Luminosidad del foco ${focoId} cambiada a nivel ${luminosity}.`);
            console.log("Respuesta del servidor:", data);
        })
        .catch((error) => {
            console.error(`Error al enviar la solicitud de luminosidad para el foco ${focoId}:`, error);
            // alert(`No se pudo cambiar la luminosidad del foco ${focoId}.`);
        });
}

// Asignar eventos a los botones de encender/apagar
document.querySelectorAll(".switch-icon-a").forEach((btn) => {
    btn.addEventListener("click", handleSwitch);
});

document.querySelectorAll(".switch-icon-b").forEach((btn) => {
    btn.addEventListener("click", handleSwitch);
});

// Asignar eventos a los controles de luminosidad
document.querySelectorAll("input[type='range']").forEach((slider) => {
    slider.addEventListener("input", handleLuminosity);
});
