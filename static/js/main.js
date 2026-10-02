/**
 * NEHRU PLACE IT SERVICES - MAIN JAVASCRIPT & CCTV CALCULATOR ENGINE
 */

document.addEventListener('DOMContentLoaded', function () {
    initThemeToggle();
    initCCTVCalculator();
    initLiveSearch();
});

function initThemeToggle() {
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (document.body) {
            document.body.setAttribute('data-theme', theme);
        }
        localStorage.setItem('theme', theme);
        
        const darkIcon = document.querySelector('.theme-icon-dark');
        const lightIcon = document.querySelector('.theme-icon-light');
        const textLabel = document.querySelector('.theme-text-label');

        if (theme === 'light') {
            if (darkIcon) darkIcon.classList.add('d-none');
            if (lightIcon) lightIcon.classList.remove('d-none');
            if (textLabel) textLabel.textContent = 'Light';
        } else {
            if (lightIcon) lightIcon.classList.add('d-none');
            if (darkIcon) darkIcon.classList.remove('d-none');
            if (textLabel) textLabel.textContent = 'Dark';
        }
    }

    const currentTheme = localStorage.getItem('theme') || 'light';
    applyTheme(currentTheme);

    const toggleBtn = document.getElementById('themeToggleBtn');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const activeTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
        });
    }
}

function initCCTVCalculator() {
    const calcForm = document.getElementById('cctvCalculatorForm');
    if (!calcForm) return;

    // Get pricing values from data attributes
    const cameraPrice = parseFloat(calcForm.dataset.cameraPrice || 2000);
    const dvrPrice = parseFloat(calcForm.dataset.dvrPrice || 5000);
    const hddPrice = parseFloat(calcForm.dataset.hddPrice || 4000);
    const powerSupplyPrice = parseFloat(calcForm.dataset.powerSupplyPrice || 800);
    const connectorPrice = parseFloat(calcForm.dataset.connectorPrice || 300);
    const cablePricePerMeter = parseFloat(calcForm.dataset.cablePrice || 25);
    const installationCharge = parseFloat(calcForm.dataset.installationCharge || 2000);
    const wiringChargePerMeter = parseFloat(calcForm.dataset.wiringCharge || 15);
    const configCharge = parseFloat(calcForm.dataset.configCharge || 1000);
    const maintenanceCharge = parseFloat(calcForm.dataset.maintenanceCharge || 1500);

    const cameraInput = document.getElementById('calcCameras');
    const cableInput = document.getElementById('calcCable');
    const includeMaintenance = document.getElementById('calcMaintenance');

    function calculate() {
        const cameraCount = parseInt(cameraInput.value) || 1;
        const cableMeters = parseInt(cableInput.value) || 50;

        // Math calculation based on DB parameters
        const totalCamerasCost = cameraCount * cameraPrice;
        const dvrCost = cameraCount > 8 ? dvrPrice * 2 : dvrPrice;
        const storageCost = hddPrice;
        const powerSupplyCost = Math.ceil(cameraCount / 4) * powerSupplyPrice;
        const connectorCost = cameraCount * connectorPrice;
        const cableCost = cableMeters * cablePricePerMeter;
        const installCost = installationCharge + ((cameraCount - 4) > 0 ? (cameraCount - 4) * 300 : 0);
        const wiringCost = cableMeters * wiringChargePerMeter;
        const configurationCost = configCharge;
        const maintenanceCost = (includeMaintenance && includeMaintenance.checked) ? maintenanceCharge : 0;

        const grandTotal = totalCamerasCost + dvrCost + storageCost + powerSupplyCost + connectorCost + cableCost + installCost + wiringCost + configurationCost + maintenanceCost;

        // Render cost breakdown in HTML
        document.getElementById('resCameraCost').innerText = '₹' + totalCamerasCost.toLocaleString('en-IN');
        document.getElementById('resDvrCost').innerText = '₹' + dvrCost.toLocaleString('en-IN');
        document.getElementById('resHddCost').innerText = '₹' + storageCost.toLocaleString('en-IN');
        document.getElementById('resPowerCost').innerText = '₹' + (powerSupplyCost + connectorCost).toLocaleString('en-IN');
        document.getElementById('resCableCost').innerText = '₹' + cableCost.toLocaleString('en-IN');
        document.getElementById('resInstallCost').innerText = '₹' + (installCost + wiringCost + configurationCost).toLocaleString('en-IN');
        document.getElementById('resGrandTotal').innerText = '₹' + grandTotal.toLocaleString('en-IN');

        // Populate hidden form field for quote request submission
        const breakdownText = `Calculated Estimate Breakdown:
- Cameras (${cameraCount} units): ₹${totalCamerasCost.toLocaleString('en-IN')}
- DVR/NVR Device: ₹${dvrCost.toLocaleString('en-IN')}
- Surveillance Storage HDD: ₹${storageCost.toLocaleString('en-IN')}
- Power Supply & Connectors: ₹${(powerSupplyCost + connectorCost).toLocaleString('en-IN')}
- Cable (${cableMeters}m @ ₹${cablePricePerMeter}/m): ₹${cableCost.toLocaleString('en-IN')}
- Installation, Wiring & Setup: ₹${(installCost + wiringCost + configurationCost).toLocaleString('en-IN')}
- Maintenance AMC: ₹${maintenanceCost.toLocaleString('en-IN')}
TOTAL ESTIMATED COST: ₹${grandTotal.toLocaleString('en-IN')}`;

        const hiddenInput = document.getElementById('id_calculation_details');
        if (hiddenInput) {
            hiddenInput.value = breakdownText;
        }
    }

    if (cameraInput) cameraInput.addEventListener('input', calculate);
    if (cableInput) cableInput.addEventListener('input', calculate);
    if (includeMaintenance) includeMaintenance.addEventListener('change', calculate);

    // Initial calculation on page load
    calculate();
}

function initLiveSearch() {
    const searchInputs = document.querySelectorAll('input[name="q"], #productSearchInput');
    if (!searchInputs.length) return;

    searchInputs.forEach(input => {
        let dropdown = input.nextElementSibling;
        if (!dropdown || (!dropdown.classList.contains('searchResultsDropdown') && dropdown.id !== 'searchResultsDropdown')) {
            dropdown = document.createElement('div');
            dropdown.className = 'glass-card shadow-lg position-absolute top-100 start-0 w-100 mt-1 d-none rounded-3 border-cyan overflow-hidden';
            dropdown.style.zIndex = '1050';
            dropdown.style.maxHeight = '400px';
            dropdown.style.overflowY = 'auto';
            dropdown.style.background = '#0f172a';
            input.parentNode.style.position = 'relative';
            input.parentNode.appendChild(dropdown);
        }

        let debounceTimer;

        input.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            const query = this.value.trim();

            if (query.length < 2) {
                dropdown.classList.add('d-none');
                dropdown.innerHTML = '';
                return;
            }

            debounceTimer = setTimeout(() => {
                fetch('/products/search-suggestions/?q=' + encodeURIComponent(query))
                    .then(res => res.json())
                    .then(data => {
                        const suggestions = data.suggestions || [];
                        if (!suggestions.length) {
                            dropdown.innerHTML = '<div class="p-3 text-muted small text-center"><i class="bi bi-info-circle me-1"></i> No matching products or specifications found</div>';
                            dropdown.classList.remove('d-none');
                            return;
                        }

                        let html = '<div class="list-group list-group-flush bg-transparent">';
                        suggestions.forEach(item => {
                            const imgHtml = item.image ? `<img src="${item.image}" alt="${item.name}" class="rounded p-1 bg-white me-2" style="width: 40px; height: 40px; object-fit: contain;">` : `<div class="rounded p-1 bg-dark text-cyan me-2 d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;"><i class="bi bi-laptop"></i></div>`;
                            html += `
                                <a href="${item.url}" class="list-group-item list-group-item-action bg-dark text-white border-secondary p-2 d-flex align-items-center justify-content-between">
                                    <div class="d-flex align-items-center text-truncate me-2">
                                        ${imgHtml}
                                        <div class="text-truncate">
                                            <div class="fw-bold text-white small text-truncate">${item.name}</div>
                                            <small class="text-cyan" style="font-size: 0.7rem;">SKU: ${item.sku} | ${item.category}</small>
                                        </div>
                                    </div>
                                    <span class="badge bg-dark border border-cyan text-cyan text-nowrap">${item.price}</span>
                                </a>
                            `;
                        });
                        html += '</div>';
                        dropdown.innerHTML = html;
                        dropdown.classList.remove('d-none');
                    })
                    .catch(() => {
                        dropdown.classList.add('d-none');
                    });
            }, 200);
        });

        document.addEventListener('click', function (e) {
            if (!input.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.classList.add('d-none');
            }
        });
    });
}
