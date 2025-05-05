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
        "Airtel Data Bundle - 50 Naira - 25MB  - 1Day",
        "Airtel Data Bundle - 100 Naira - 75MB - 1Day",
        "Airtel Data Bundle - 200 Naira - 200MB - 3Days",
        "Airtel Data Bundle - 300 Naira - 350MB - 7 Days",
        "Airtel Data Bundle - 500 Naira - 750MB - 14 Days",
        "Airtel Data Bundle - 1,000 Naira - 1.5GB - 30 Days",
        "Airtel Data Bundle - 1,500 Naira - 3GB - 30 Days",
        "Airtel Data Bundle - 2,000 Naira - 4.5GB - 30 Days",
        "Airtel Data Bundle - 3,000 Naira - 8GB - 30 Days",
        "Airtel Data Bundle - 4,000 Naira - 11GB - 30 Days",
        "Airtel Data Bundle - 5,000 Naira - 15GB - 30 Days",
        "Airtel Binge Data - 1,500 Naira (7 Days) - 6GB",
        "Airtel Data Bundle - 10,000 Naira - 40GB - 30 Days",
        "Airtel Data Bundle - 15,000 Naira - 75GB - 30 Days",
        "Airtel Data Bundle - 20,000 Naira - 110GB - 30 Days"
    ],
    "Glo": {
        "Glo Data": [
            "Glo Data N100 -  105MB - 2 day",
            "Glo Data N200 -  350MB - 4 days",
            "Glo Data N500 -  1.05GB - 14 days",
            "Glo Data N1000 -  2.5GB - 30 days",
            "Glo Data N2000 -  5.8GB - 30 days",
            "Glo Data N2500 -  7.7GB - 30 days",
            "Glo Data N3000 -  10GB - 30 days",
            "Glo Data N4000 -  13.25GB - 30 days",
            "Glo Data N5000 -  18.25GB - 30 days",
            "Glo Data N8000 -  29.5GB - 30 days",
            "Glo Data N10000 -  50GB - 30 days",
            "Glo Data N15000 -  93GB - 30 days",
            "Glo Data N18000 -  119GB - 30 days",
            "Glo Data N1500 -  4.1GB - 30 days",
            "Glo Data N20000 -  138GB - 30 days"
        ],
        "Glo SME Data": [
            "Glo Data (SME) N50 -  200MB - 14 days",
            "Glo Data (SME) N125 - 500MB 14 days",
            "Glo Data (SME) N125 - 500MB 30 days",
            "Glo Data (SME) N250 - 1GB 30 days",
            "Glo Data (SME) N500 - 2GB 30 days"
        ]
    },
    "9mobile": {
        "9mobile Data": [
            "9mobile Data - 100 Naira - 100MB - 1 day",
            "9mobile Data - 200 Naira - 650MB - 1 day",
            "9mobile Data - 500 Naira - 500MB - 30 Days",
            "9mobile Data - 1000 Naira - 1.5GB - 30 days",
            "9mobile Data - 2000 Naira - 4.5GB Data - 30 Days",
            "9mobile Data - 5000 Naira - 15GB Data - 30 Days",
            "9mobile Data - 10000 Naira - 40GB - 30 days",
            "9mobile Data - 15000 Naira - 75GB - 30 Days",
            "9mobile Data - 27,500 Naira - 30GB - 90 days",
            "9mobile Data - 55,000 Naira - 60GB - 180 days",
            "9mobile Data - 110,000 Naira - 120GB - 365 days"
    
        ],
        "9mobile SME Data": [
            "9mobile Sme Data - 100 Naira - 100MB - 1 day",
            "9mobile Sme Data - 200 Naira -650MB - 2 day",
            "9mobile Sme Data - 500 Naira - 500MB - 30 Days"
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
            populateDualPlans(dataPlans[networkName]);
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
    populateDualPlans(selectedPlans);
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


document.getElementById('dataPlan').addEventListener('change', function () {
    const selectedPlan = this.value;

    let amount;
    const amountField = document.getElementById('amountField');

    // Clean up the selected plan (remove commas if any)
    const cleanedPlan = selectedPlan.replace(/,/g, '');

    // Check for Airtel and 9mobile data plans where amount comes before "Naira"
    if (cleanedPlan.includes("Naira")) {
        // For Airtel and 9mobile, the amount comes before "Naira"
        const regex = /(\d+)\s*Naira/;
        const match = cleanedPlan.match(regex);
        if (match) {
            amount = match[1];  // Extract the amount before "Naira"
        }
    } 
    // Check for MTN and Glo data plans where amount comes after "N"
    else if (cleanedPlan.startsWith('N')) {
        // For MTN and Glo, the amount comes after "N"
        const regex = /^N(\d+)/;
        const match = cleanedPlan.match(regex);
        if (match) {
            amount = match[1];  // Extract the amount after "N"
        }
    } 
    // Special case for Glo Data (SME) plans
    else if (cleanedPlan.includes("Glo Data") && (cleanedPlan.includes("(SME)") || cleanedPlan.startsWith("Glo Data"))) {
        // Regular expression to match "Glo Data" or "Glo Data (SME)" followed by the amount
        const regex = /Glo\s+Data\s*(\(SME\))?\s*N(\d+)/;  // Match "Glo Data N1000" or "Glo Data (SME) N500"

        const match = cleanedPlan.match(regex);
        if (match) {
            amount = match[2];  // Extract the numeric part after "Data" or "SME N"
        }
    }

    // If the amount is found, update the amount field and disable it
    if (amount) {
        // Display the amount with "N" format (e.g., N1000)
        amountField.value = `N${amount}`;
        amountField.disabled = true;  // Disable the field so the user can't edit it
    }
});





// Extract amount from a plan string (handles different formats)
function extractAmount(plan) {
    const cleaned = plan.replace(/,/g, '');
    let match = cleaned.match(/N(\d+)/) || cleaned.match(/(\d+)\s*Naira/);
    return match ? parseInt(match[1]) : null;
}

// Replace amount in a plan string
function replaceAmount(plan, newAmount) {
    return plan.replace(/N(\d+)/, `N${newAmount}`).replace(/(\d+)\s*Naira/, `${newAmount} Naira`);
}

// Populate both dataPlan and dataPlanPlus with original and +₦10 versions
function populateDualPlans(plans) {
    const dataPlan = document.getElementById('dataPlan');
    const dataPlanPlus = document.getElementById('dataPlanPlus');
    dataPlan.innerHTML = '';
    dataPlanPlus.innerHTML = '';

    // Append default separately to avoid cloneNode issues
    const defaultOption1 = document.createElement('option');
    defaultOption1.textContent = 'Select Data Plan';
    defaultOption1.disabled = true;
    defaultOption1.selected = true;
    defaultOption1.value = '';

    const defaultOption2 = document.createElement('option');
    defaultOption2.textContent = 'Select Data Plan';
    defaultOption2.disabled = true;
    defaultOption2.selected = true;
    defaultOption2.value = '';

    dataPlan.appendChild(defaultOption1);
    dataPlanPlus.appendChild(defaultOption2);


    plans.forEach(plan => {
        const amount = extractAmount(plan);
        if (!amount) return;

        // Original
        const option = document.createElement('option');
        option.value = plan;
        option.textContent = plan;
        dataPlan.appendChild(option);

        // +₦10 version
        const newPlan = replaceAmount(plan, amount + 10);
        const optionPlus = document.createElement('option');
        optionPlus.value = newPlan;
        optionPlus.textContent = newPlan;
        dataPlanPlus.appendChild(optionPlus);
    });

    // Synchronize selections
    dataPlan.addEventListener('change', function () {
        const selected = this.selectedIndex;
        dataPlanPlus.selectedIndex = selected;
        updateAmountFromPlan(this.value);
    });

    dataPlanPlus.addEventListener('change', function () {
        const selected = this.selectedIndex;
        dataPlan.selectedIndex = selected;
        updateAmountFromPlan(this.value);
    });
}

// Update amount field when plan is selected
function updateAmountFromPlan(planText) {
    const amount = extractAmount(planText);
    const amountField = document.getElementById('amountField');
    if (amount) {
        amountField.value = `N${amount}`;
        amountField.disabled = true;
    }
}
