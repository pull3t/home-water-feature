document.addEventListener('DOMContentLoaded', function () {
    const pumpToggle = document.getElementById('pumpToggle');
    const lightToggle = document.getElementById('lightToggle');
    const automationToggle = document.getElementById('automationToggle');
    const automationOptions = document.getElementById('automationOptions');
    const timeBasedOptions = document.getElementById('timeBasedOptions');
    const lightBasedOptions = document.getElementById('lightBasedOptions');
    const saveAutomation = document.getElementById('saveAutomation');

    // Helper: Show/hide automation options
    function updateAutomationDisplay() {
        const enabled = automationToggle.checked;
        automationOptions.style.display = enabled ? 'block' : 'none';

        const selectedMode = document.querySelector('input[name="automationType"]:checked')?.value;
        timeBasedOptions.style.display = selectedMode === 'time' ? 'block' : 'none';
        lightBasedOptions.style.display = selectedMode === 'light' ? 'block' : 'none';
    }

    // Initial load
    updateAutomationDisplay();

    // Event Listeners
    automationToggle?.addEventListener('change', updateAutomationDisplay);
    document.querySelectorAll('input[name="automationType"]').forEach(radio => {
        radio.addEventListener('change', updateAutomationDisplay);
    });

    pumpToggle?.addEventListener('change', () => toggleDevice('pump'));
    lightToggle?.addEventListener('change', () => toggleDevice('light'));

    saveAutomation?.addEventListener('click', function () {
        const selectedType = document.querySelector('input[name="automationType"]:checked')?.value;

        fetch('/api/update_automation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mode: selectedType,
                time_on: document.getElementById('timeOn').value,
                time_off: document.getElementById('timeOff').value,
                time_pump: document.getElementById('timePump').checked,
                time_light: document.getElementById('timeLight').checked,
                lux_threshold: document.getElementById('luxThreshold').value,
                lux_pump: document.getElementById('luxPump').checked,
                lux_light: document.getElementById('luxLight').checked
            })
        });
    });

    function toggleDevice(device) {
        fetch('/api/toggle_device', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ device: device })
        });
    }

    function updateStatus() {
        fetch('/api/get_status')
            .then(res => res.json())
            .then(data => {
                document.getElementById('lux').textContent = data.lux;
                document.getElementById('datetime').textContent = data.datetime;
            });
    }

    // Periodic update
    setInterval(updateStatus, 5000);
});
