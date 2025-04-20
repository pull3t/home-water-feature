document.getElementById('automationForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const automation = {
        enabled: document.getElementById('automationToggle').checked,
        type: document.querySelector('input[name="automationType"]:checked').value,
        startTime: document.getElementById('startTime').value,
        endTime: document.getElementById('endTime').value,
        pump: document.getElementById('autoPump').checked,
        light: document.getElementById('autoLight').checked,
        luxThreshold: document.getElementById('luxThreshold').value
    };

    fetch('/update-automation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(automation)
    })
    .then(res => res.json())
    .then(data => alert('Settings updated successfully'))
    .catch(err => alert('Error updating settings'));
});
