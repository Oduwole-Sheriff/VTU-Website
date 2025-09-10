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
        "N20000 110GB - 30 days",
        "N1500 3GB - 30 days",
        "MTN N10,000 25GB SME Mobile Data (1 Month)",
        "MTN N50,000 165GB SME Mobile Data (2-Months)",
        "MTN N100,000 360GB SME Mobile Data (3 Months)",
        "MTN N450,000 4.5TB Mobile Data (1 Year)",
        "MTN N100,000 1TB Mobile Data (1 Year)",
        "MTN N600 2.5GB - 2 days",
        "MTN N22000 120GB Monthly Plan + 80mins",
        "MTN 100GB 2-Month Plan",
        "MTN N30,000 160GB 2-Month Plan",
        "MTN N50,000 400GB 3-Month Plan",
        "MTN N75,000 600GB 3-Months Plan",
        "MTN N300 Xtratalk Weekly Bundle",
        "MTN N500 Xtratalk Weekly Bundle",
        "MTN N1000 Xtratalk Monthly Bundle",
        "MTN N2000 Xtratalk Monthly Bundle",
        "MTN N5000 Xtratalk Monthly Bundle",
        "MTN N10000 Xtratalk Monthly Bundle",
        "MTN N15000 Xtratalk Monthly Bundle",
        "MTN N20000 Xtratalk Monthly Bundle",
        "MTN N800 3GB - 2 days",
        "MTN N2000 7GB - 7 days",
        "MTN N200 Xtradata",
        "MTN N200 Xtratalk - 3 days"
    ],
    "Airtel": [
        "Airtel Data Bundle - 50 Naira - 25MB - 1Day",
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
        "Airtel Data Bundle - 20,000 Naira - 110GB - 30 Days",
        "Airtel Data - 600 Naira - 1GB - 14 days",
        "Airtel Data - 1000 Naira - 1.5GB - 7 days",
        "Airtel Data - 2000 Naira - 7GB - 7 days",
        "Airtel Data - 5000 Naira - 25GB - 7 days",
        "Airtel Data - 400 Naira - 1.5GB - 1 day",
        "Airtel Data - 800 Naira - 3.5GB - 2 days",
        "Airtel Data - 6000 Naira - 23GB - 30 days",
        "600 Naira Voice Bundle",
        "1200 Naira Voice Bundle",
        "3000 Naira Voice Bundle",
        "6000 Naira Voice Bundle"
    ],
    "Glo": {
        "Glo Data": [
            "Glo Data N100 -  105MB - 2 day",
            "Glo Data N200 -  350MB - 4 days",
            "Glo Data N500 -  1.05GB - 14 days",
            "Glo Data N1000 -  2.5GB - 30 days",
            "Glo Data N1500 -  4.1GB - 30 days",
            "Glo Data N2000 -  5.8GB - 30 days",
            "Glo Data N2500 -  7.7GB - 30 days",
            "Glo Data N3000 -  10GB - 30 days",
            "Glo Data N4000 -  13.25GB - 30 days",
            "Glo Data N5000 -  18.25GB - 30 days",
            "Glo Data N8000 -  29.5GB - 30 days",
            "Glo Data N10000 -  50GB - 30 days",
            "Glo Data N15000 -  93GB - 30 days",
            "Glo Data N18000 -  119GB - 30 days",
            "Glo Data N20000 -  138GB - 30 days",
            "45MB + 5MB Night N50 Oneoff",
            "115MB + 35MB Night N100 Oneoff",
            "240MB + 110MB Night N200 Oneoff",
            "800MB + 1GB Night N500 Oneoff",
            "1.9GB + 2GB Night N1000 Oneoff",
            "3.5GB + 4GB Night N1500 Oneoff",
            "5.2GB + 4GB Night N2000 Oneoff",
            "6.8GB + 4GB Night N2500 Oneoff",
            "10GB + 4GB Night N3000 Oneoff",
            "14GB + 4GB Night N4000 Oneoff",
            "20GB + 4GB Night N5000 Oneoff",
            "27.5GB + 2GB Night N8000 Oneoff",
            "46GB + 4GB Night N10000 Oneoff",
            "86GB + 7GB Night N15000 Oneoff",
            "109GB + 10GB Night N18000 Oneoff",
            "126GB + 12GB Night N20000 Oneoff",

            "N300 1GB Special",
            "N500 2GB Special",
            "N1500 7GB Special",

            "N500 3GB Weekend",

            "N30000 225GB Glo Mega Oneoff",
            "N36000 300GB Glo Mega Oneoff",
            "N50000 425GB Glo Mega Oneoff",
            "N60000 525GB Glo Mega Oneoff",
            "N75000 675GB Glo Mega Oneoff",
            "N100000 1TB Glo Mega Oneoff",

            "Glo TV VOD 500MB 3days Oneoff",
            "Glo TV VOD 2GB 7days Oneoff",
            "Glo TV VOD 6GB 30days Oneoff",
            "Glo TV Lite 2GB Oneoff",
            "Glo TV Max 6GB Oneoff",

            "WTF N25 100MB Oneoff",
            "WTF N50 200MB Oneoff",
            "WTF N100 500MB Oneoff",

            "Telegram N25 20MB Oneoff",
            "Telegram N50 50MB Oneoff",
            "Telegram N100 125MB Oneoff",

            "Instagram N25 20MB Oneoff",
            "Instagram N50 50MB Oneoff",
            "Instagram N100 125MB Oneoff",

            "Tiktok N25 20MB Oneoff",
            "Tiktok N50 50MB Oneoff",
            "Tiktok N100 125MB Oneoff",

            "Opera N25 25MB Oneoff",
            "Opera N50 100MB Oneoff",
            "Opera N100 300MB Oneoff",

            "Youtube N50 100MB Oneoff",
            "Youtube N100 200MB Oneoff",
            "Youtube N250 500MB Oneoff",
            "Youtube N50 500MB Oneoff",
            "Youtube N130 1.5GB Oneoff",
            "Youtube N50 500MB Night Oneoff",
            "Youtube N200 2GB Night Oneoff",

            "Glo MyG N100 400 MB OneOff (Whatsapp, Instagram, Snapchat, Boomplay, Audiomac, GloTV, Tiktok)",
            "Glo MyG N300 1 GB OneOff (Whatsapp, Instagram, Snapchat, Boomplay, Audiomac, GloTV, Tiktok)",
            "Glo MyG N500 1.5 GB OneOff (Whatsapp, Instagram, Snapchat, Boomplay, Audiomac, GloTV, Tiktok)",
            "Glo MyG N1000 3.5 GB OneOff (Whatsapp, Instagram, Snapchat, Boomplay, Audiomac, GloTV, Tiktok)"
        ],
        "Glo SME Data": [         
            "Glo Data (SME) N70 -  200MB - 14 days",
            "Glo Data (SME) N160 - 500MB 14 days",
            "Glo Data (SME) N320 - 1GB 30 days",
            "Glo Data (SME) N640 - 2GB 30 days",
            "Glo Data (SME) N960 - 3GB 30 days",
            "Glo Data (SME) N1600 - 5GB 30 days",
            "Glo Data (SME) N3100 - 10GB - 30 Days",
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
            "9mobile Data - 110,000 Naira - 120GB - 365 days",
            "9mobile 1GB + 100MB (1 day) - 300 Naira",
            "9mobile 11GB (7GB+ 4GB Night) - 2,500 Naira - 30 days",
            "9mobile 35 GB - 7,000 Naira - 30 days",
            "9mobile 125GB - 20,000 Naira - 30 days",
            "9mobile 4GB (2GB + 2GB Night) - 1000 Naira",
            "9mobile 7GB (6GB+1GB Night) - 7 days",
            "9mobile 200MB (100MB + 100MB night) + 300secs - 1 day"
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
