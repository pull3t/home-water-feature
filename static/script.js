document.addEventListener('DOMContentLoaded', function () {
    const automationToggle = document.getElementById('automation-toggle');
    const timeRadio = document.querySelector('input[value="time"]');
    const luxRadio = document.querySelector('input[value="light"]');
    const timeFields = document.querySelector('fieldset:nth-of-type(1)');
    const luxFields = document.querySelector('fieldset:nth-of-type(2)');

    function updateVisibility() {
        const enabled = automationToggle.checked;
        timeFields.style.display = enabled && timeRadio.checked ? 'block' : 'none';
        luxFields.style.display = enabled && luxRadio.checked ? 'block' : 'none';
    }

    automationToggle.addEventListener('change', updateVisibility);
    timeRadio.addEventListener('change', updateVisibility);
    luxRadio.addEventListener('change', updateVisibility);

    updateVisibility(); // Initial state
});
