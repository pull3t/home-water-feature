document.addEventListener('DOMContentLoaded', function () {
    const timeSection = document.getElementById('time_automation_section');
    const lightSection = document.getElementById('light_automation_section');
    const radios = document.querySelectorAll('input[name="automation_mode"]');

    function updateVisibility() {
        const selectedMode = document.querySelector('input[name="automation_mode"]:checked').value;
        timeSection.style.display = selectedMode === 'time' ? 'block' : 'none';
        lightSection.style.display = selectedMode === 'light' ? 'block' : 'none';
    }

    radios.forEach(radio => radio.addEventListener('change', updateVisibility));
    updateVisibility();  // Set on page load
});
