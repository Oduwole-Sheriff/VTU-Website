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
    "9mobile": {
        "9mobile Data": [
            "N100 100MB - 24 hrs",
            "N500 1GB - 2 days",
            "N1500 3GB - 7 days",
            "N2500 10GB - 30 days",
            "N5000 20GB - 30 days"
        ],
        "9mobile SME Data": [
            "N100 100MB - 24 hrs",
            "N500 1GB - 2 days",
            "N1000 3GB - 7 days",
            "N3000 10GB - 30 days",
            "N7000 25GB - 30 days"
        ]
    }
};

// Display the form and set the network when a circle is clicked
document.querySelectorAll('.circle').forEach(circle => {
    circle.addEventListener('click', function () {
        const networkName = this.getAttribute('data-network');
        const formContainer = document.getElementById('formContainer');
        const networkHeading = document.getElementById('networkName');
        const dataPlanSelect = document.getElementById('dataPlan');
        const gloDataTypeContainer = document.getElementById('gloDataTypeContainer');
        const nineMobileDataTypeContainer = document.getElementById('nineMobileDataTypeContainer');
        const gloDataTypeSelect = document.getElementById('gloDataType');
        const nineMobileDataTypeSelect = document.getElementById('nineMobileDataType');
        const amountField = document.getElementById('amountField');  // Get the amount field
        
        formContainer.style.display = 'block';
        document.getElementById('network').value = networkName;
        networkHeading.innerHTML = `${networkName} Data Bundles`;  // Add network name before "Data Bundles"
        
        // Clear the Amount field when switching networks
        amountField.value = '';  // Clear the amount field
        
        // Populate the "Data Plan" dropdown based on the selected network
        dataPlanSelect.innerHTML = ''; // Clear previous options
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.disabled = true;
        defaultOption.selected = true;
        defaultOption.textContent = 'Select Data Plan';
        dataPlanSelect.appendChild(defaultOption);

        if (networkName === "Glo") {
            // Show Glo-specific Data Type dropdown
            gloDataTypeContainer.style.display = 'block';
            nineMobileDataTypeContainer.style.display = 'none';

            // Populate the data plans based on the selected data type for Glo
            const selectedDataType = gloDataTypeSelect.value;
            populateDataPlans(selectedDataType, networkName);
        } else if (networkName === "9mobile") {
            // Show 9mobile-specific Data Type dropdown
            nineMobileDataTypeContainer.style.display = 'block';
            gloDataTypeContainer.style.display = 'none';

            // Populate the data plans based on the selected data type for 9mobile
            const selectedDataType = nineMobileDataTypeSelect.value;
            populateDataPlans(selectedDataType, networkName);
        } else {
            // For other networks (MTN, Airtel), hide the Data Type field
            gloDataTypeContainer.style.display = 'none';
            nineMobileDataTypeContainer.style.display = 'none';
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

// Function to populate data plans for the selected data type (Glo or 9mobile)
function populateDataPlans(dataType, networkName) {
    const dataPlanSelect = document.getElementById('dataPlan');
    dataPlanSelect.innerHTML = ''; // Clear previous options
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.disabled = true;
    defaultOption.selected = true;
    defaultOption.textContent = 'Select Data Plan';
    dataPlanSelect.appendChild(defaultOption);

    // Add data plans based on the selected data type for Glo or 9mobile
    const selectedPlans = dataPlans[networkName][dataType];
    selectedPlans.forEach(plan => {
        const option = document.createElement('option');
        option.value = plan;
        option.textContent = plan;
        dataPlanSelect.appendChild(option);
    });
}

// Listen for changes to the Data Type dropdown
document.getElementById('gloDataType')?.addEventListener('change', function () {
    const selectedDataType = this.value;
    const networkName = document.getElementById('network').value;
    populateDataPlans(selectedDataType, networkName);
});

document.getElementById('nineMobileDataType')?.addEventListener('change', function () {
    const selectedDataType = this.value;
    const networkName = document.getElementById('network').value;
    populateDataPlans(selectedDataType, networkName);
});

// Function to update the Amount field based on selected data plan
document.getElementById('dataPlan').addEventListener('change', function () {
    const selectedPlan = this.value;

    // Extract the amount from the selected data plan
    const regex = /^N(\d+)/;  // Regex to extract the amount (e.g., "N1000" -> 1000)
    const match = selectedPlan.match(regex);

    if (match) {
        const amount = match[1];  // Get the amount part
        const amountField = document.getElementById('amountField');
        
        // Set the value of the amount field and disable it
        amountField.value = `N${amount}`;  // Format with "N"
        amountField.disabled = true; // Disable the field so the user can't edit it
    }
});
