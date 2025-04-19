function toggleDevice(device) {
    fetch(`/toggle/${device}`, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`${device}_status`).innerText = data.state ? "ON" : "OFF";
    });
}

function updateRules() {
    fetch('/update_rules', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            pump_enabled: document.getElementById('pump_enabled').checked,
            pump_on_time: document.getElementById('pump_on_time').value,
            pump_off_time: document.getElementById('pump_off_time').value,
            light_enabled: document.getElementById('light_enabled').checked,
            lux_threshold: document.getElementById('lux_threshold').value
        })
    }).then(response => response.json())
      .then(data => alert('Automation rules updated successfully!'));
}

setInterval(() => {
    fetch('/lux').then(res => res.json())
    .then(data => document.getElementById('lux').innerText = data.lux.toFixed(2));
}, 5000);
