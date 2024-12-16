// Data plans for each network
const dataPlans = {
    "MTN": [
        "N100 100MB - 24 hrs",
        "N200 200MB - 2 days",
        "N1000 1.5GB - 30 days",
        "N2000 4.5GB - 30 days",
        "N1500 6GB - 7 days",
        "N2500 6GB - 30 days",
        "N3000 8GB - 30 days",
        "N3500 10GB - 30 days",
        "N5000 15GB - 30 days",
        "N6000 20GB - 30 days",
        "N10000 40GB - 30 days",
        "N15000 75GB - 30 days",
        "N20000 110GB - 30 days"
    ],
    "Airtel": [
        "N100 100MB - 24 hrs",
        "N200 200MB - 2 days",
        "N500 1GB - 3 days",
        "N1500 3GB - 30 days",
        "N2500 6GB - 30 days",
        "N5000 15GB - 30 days",
        "N10000 40GB - 30 days"
    ],
    "Glo": {
        "Glo Data": [
            "N150 150MB - 24 hrs",
            "N500 1GB - 3 days",
            "N1500 5GB - 30 days",
            "N2500 10GB - 30 days",
            "N5000 25GB - 30 days"
        ],
        "Glo SME Data": [
            "N100 100MB - 24 hrs",
            "N500 1GB - 3 days",
            "N1000 3GB - 7 days",
            "N3000 10GB - 30 days",
            "N7000 25GB - 30 days"
        ]
    },
    "9mobile": [
        "N100 100MB - 24 hrs",
        "N500 1GB - 2 days",
        "N1500 3GB - 7 days",
        "N2500 10GB - 30 days",
        "N5000 20GB - 30 days"
    ]
};

// Display the form and set the network when a circle is clicked
document.querySelectorAll('.circle').forEach(circle => {
    circle.addEventListener('click', function () {
        const networkName = this.getAttribute('data-network');
        const formContainer = document.getElementById('formContainer');
        const networkHeading = document.getElementById('networkName');
        const dataPlanSelect = document.getElementById('dataPlan');
        const dataTypeContainer = document.getElementById('dataTypeContainer');
        const dataTypeSelect = document.getElementById('dataType');
        
        formContainer.style.display = 'block';
        document.getElementById('network').value = networkName;
        networkHeading.innerHTML = `${networkName} Data Bundles`;  // Add network name before "Data Bundles"
        
        // Populate the "Data Plan" dropdown based on the selected network
        dataPlanSelect.innerHTML = ''; // Clear previous options
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.disabled = true;
        defaultOption.selected = true;
        defaultOption.textContent = 'Select Data Plan';
        dataPlanSelect.appendChild(defaultOption);

        if (networkName === "Glo") {
            // Display the Data Type dropdown for Glo
            dataTypeContainer.style.display = 'block';

            // Populate the data plans based on the selected data type
            const selectedDataType = dataTypeSelect.value;
            populateDataPlans(selectedDataType);
        } else {
            // For other networks, hide the Data Type field
            dataTypeContainer.style.display = 'none';
            dataPlans[networkName].forEach(plan => {
                const option = document.createElement('option');
                option.value = plan;
                option.textContent = plan;
                dataPlanSelect.appendChild(option);
            });
        }

        // Remove checkmarks, selected, and blinking states from all circles
        document.querySelectorAll('.circle').forEach(c => {
            c.classList.remove('selected');
        });

        // Add checkmark and selected state to the clicked circle
        this.classList.add('selected');
    });
});

// Function to populate data plans for the selected data type
function populateDataPlans(dataType) {
    const dataPlanSelect = document.getElementById('dataPlan');
    dataPlanSelect.innerHTML = ''; // Clear previous options
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.disabled = true;
    defaultOption.selected = true;
    defaultOption.textContent = 'Select Data Plan';
    dataPlanSelect.appendChild(defaultOption);

    // Add data plans based on the selected data type for Glo
    const selectedPlans = dataPlans["Glo"][dataType];
    selectedPlans.forEach(plan => {
        const option = document.createElement('option');
        option.value = plan;
        option.textContent = plan;
        dataPlanSelect.appendChild(option);
    });
}

// Listen for changes to the Data Type dropdown
document.getElementById('dataType')?.addEventListener('change', function () {
    const selectedDataType = this.value;
    populateDataPlans(selectedDataType);
});
