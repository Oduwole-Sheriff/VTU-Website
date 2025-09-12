// Data plans for each network
const dataPlans = {
    "MTN": [
        "110MB Daily Plan (1 Day) - N100",
        "230MB Daily Plan (1 Day) - N200",
        "1.5GB Weekly Plan (7 Days) - N1,000",
        "7GB Monthly Plan - N3,500",
        "3.5GB Weekly Plan (7 Days) - N1,500",
        "16.5GB Monthly Plan",
        "20GB Monthly Plan",
        "30GB Monthly Broadband Plan - N9,000",
        "36GB Monthly Plan",
        "75GB Monthly Plan",
        "2.7GB + 2mins + 2GB All Night Streaming + 200MB YouTube Music, Monthly Plan - N2000",
        "1.8GB + 6mins + 5 SMS, Weekly plan - N1500",
        "MTN N24,000 120GB  - 30days",
        "480GB 3-Month Plan - N90,000",
        "MTN N500 1GB + 1.5mins - 1 day",
        "1GB+5mins Weekly Plan",
        "600MB Xtra Bundle Weekly Data (7 Days) - N500",
        "2GB + 2 Mins Monthly Plan - N1,500",
        "12.5GB Monthly Plan - N5,500",
        "12.5GB + 36mins + 15 SMS, Weekly plan - 5500",
        "MTN N900 2.5GB - 2 days",
        "150GB 2-Month Plan",
        "MTN N3,500 11GB  - 7 days",
        "500MB Daily Plan (1 Day) - N350",
        "1.5GB Daily Plan (2 Days) - N600",
        "2GB Daily Plan (2 Days) - N750",
        "2.7GB Xtra Bundle Monthly Plan",
        "MTN N4,500 10GB + 10mins  - 30 days",
        "65GB Monthly Plan (30 Days) - N16,000",
        "500MB + 1GB YouTube (7 Days) - N500",
        "MTN N1000 3.2GB - 2 days",
        "MTN N2500 6GB - 7 days",
        "MTN N2500 3.5GB +5mins Monthly Plan",
        "60GB Monthly HyNetFlex Plan - N14,500",
        "450GB 3-Month Broadband Plan - N75,000",
        "30GB Monthly Broadband Plan - N9,000",
        "2.5GB Daily Plan - 750 Naira",
        "20GB Weekly Plan - 5,000 Naira",
        "MTN N1800 7GB - (2 Days)",
        "MTN N30,000 150GB + 2GB daily - 5G Router Data (30 Days)",
        "MTN N35,000 165GB Monthly Data Plan (30 Days)",
        "MTN N37,500 200GB + 5GB Youtube/MSTeams/Zoom - 5G Router Data (30 Days)",
        "MTN 260GB + 2GB daily upon exhausting main bundle - N45,000",
        "MTN 1.5TB - N225,000"
    ],
    "Airtel": [
        "250MB Night Plan (12 - 5 AM) - 50 Naira  - 1Day",
        "200MB Social Plan (2 Days) - 100 Naira - 1Day",
        "230MB Daily Plan (2 Days) - 200 Naira - 200MB - 1Day",
        "Airtel Data - 100 Naira - 110MB - 1 Day",
        "500MB Weekly Plan (7 Days) - 500 Naira",
        "1.5GB Weekly Plan + Youtube & Social Plans (7 Days) - 1,000 Naira",
        "3.5GB Weekly Plan + Youtube & Social Platform (7 Days) - 1,500 Naira",
        "3GB Monthly Plan + Youtube & Social Plan (30 Days)- 2,000 Naira",
        "8GB Monthly Plan + Youtube & Social Plan (30 Days) - 3,000 Naira",
        "10GB Monthly Plan + Youtube & Social Plan (30 Days) - 4,000 Naira",
        "13GB Monthly Plan + Youtube & Social Plan (30 Days) - 5,000 Naira",
        "5GB Binge Plan + Youtube & Social Platforms Data (2 Day) - 1,500 Naira",
        "35GB Monthly Plan + Youtube & Social Plan (30 Days) - 10,000 Naira",
        "60GB Monthly Plan + Youtube & Social Plan (30 Days) - 15,000 Naira",
        "210GB Data (30 Days) - 40,000 Naira",
        "350GB Monthly Plan + Youtube & Social Plan (120 Days) - 60,000 Naira",
        "680GB Data (365 Days) - 100,000 Naira",
        "100GB Monthly Plan + Youtube & Social Plan (30 Days) - 20,000 Naira",
        "4GB Monthly Plan + Youtube & Social Plan (30 Days) - 2,500 Naira",
        "25GB Monthly Plan + Youtube & Social Plan (30 Days) - 8,000 Naira",
        "160GB Monthly Plan (30 Days) - 30,000 Naira",
        "200GB Monthly Plan (90 Days) - 50,000 Naira",
        "1.5GB Binge Plan + Youtube & Social Plan Data (2 Days) - 600 Naira",
        "3.2GB Binge Plan + Youtube & Social Plans Data (2 Days)  - 1000 Naira",
        "10GB Weekly Plan + Youtube & Social Platform (7 Days) - 3000 Naira",
        "18GB Weekly Plan + Youtube & Social Platform (7 Days) - 5000 Naira",
        "500 Naira Binge Plan -",
        "1GB Weekly Plan (7 Days) - 800 Naira",
        "18GB Monthly Plan + Youtube & Social Plan (30 Days) - 6000 Naira",
        "75MB Daily Plan (1 Day) - 75 Naira",
        "300MB Daily Plan (1 Day) - 300 Naira",
        "1GB Social Plan Plan (3 Days) - 300 Naira",
        "2GB Binge Plan + Youtube & Social Plan Data (2 Days) - 750 Naira",
        "2GB Monthly Plan + Youtube & Social Plan (30 Days) - 1,500 Naira",
        "6GB Weekly Plan + Youtube & Social Platform (7 Days) - 2,500 Naira",
        "13GB MIFI 5 Data - MiFi Only (30 Days) - 5,000 Naira",
        "35GB MIFI 10 Data - MiFi Only (30 Days) - 10,000 Naira",
        "60GB MIFI 15 Data - MiFi Only (30 Days) - 15,000 Naira",
        "100GB Unlimited Uiltra 20 - Router Only (30 Days) - 20,000 Naira",
        "Unlimited 20MBPS Data - Router Only (30 Days) - 30,000 Naira",
        "Unlimited 60MBPS Data - Router Only (30 Days) - 50,000 Naira",
        "Unlimited 60MBPS Data - Router Only (90 Days) - 80,000 Naira",
        "Unlimited 60MBPS Data - Router Only (90 Days) - 135,000 Naira",
        "Unlimited 20MBPS Data - Router Only (120 Days) - 150,000 Naira",
        "1.5GB Social Plan - 500 Naira",
        "500MB Daily Plan (2 Days) - 350 Naira - 500MB - 2 Days"
    ],
    "Glo": {
        "Glo Data": [
            "40MB - N50 Oneoff",
            "83MB - N100 Oneoff",
            "260MB - N200 Oneoff",
            "1.5GB - N500 Oneoff",
            "2.6GB - N1000 Oneoff",
            "5GB - N1500 Oneoff",
            "6.25GB - N2000 Oneoff",
            "7.5GB - N2500 Oneoff",
            "11GB - N3000 Oneoff",
            "14GB - N4000 Oneoff",
            "18GB - N5000 Oneoff",
            "29GB - N8000 Oneoff",
            "40GB - N10000 Oneoff",
            "1.75GB - Sunday N200",
            "2GB - Special N500",
            "6GB - Special N1500",
            "2.2GB - Weekend N500",
            "165GB - Mega N30000 Oneoff",
            "220GB - Mega N36000 Oneoff",
            "320GB - Mega N50000 Oneoff",
            "380GB - Mega N60000 Oneoff",
            "475GB - Mega N75000 Oneoff",
            "Glo TV VOD 500 MB 3days Oneoff",
            "Glo TV VOD 2GB 7days Oneoff",
            "Glo TV VOD 6GB 30days Oneoff",
            "Glo TV Lite 2GB Oneoff",
            "Glo TV Max 6 GB Oneoff",
            "300MB - GloMyG N100 OneOff",
            "Glo MyG N300 1 GB OneOff (Whatsapp, Instagram, Snapchat, Boomplay, Audiomac, GloTV, Tiktok)",
            "Glo MyG N500 1.5 GB OneOff (Whatsapp, Instagram, Snapchat, Boomplay, Audiomac, GloTV, Tiktok)",
            "Glo MyG N1000 3.5 GB OneOff (Whatsapp, Instagram, Snapchat, Boomplay, Audiomac, GloTV, Tiktok)",
            "235MB - Camp-Boost N100 Oneoff",
            "480MB - Camp-Boost N200 Oneoff",
            "2GB - Camp-Boost N500 Oneoff",
            "4.2GB - Camp-Boost N1000 Oneoff",
            "10.6GB - Camp-Boost 2000 Oneoff",
            "32GB - Camp-Boost N5000 Oneoff",
        ],
        "Glo SME Data": [         
            "Glo Data (SME)  1GB - 295 Naira - 3 days",
            "Glo Data (SME) 3GB - 890 Naira - 3 days",
            "Glo Data (SME) 5GB - 1,485 Naira - 3 days",
            "Glo Data (SME) 1GB - 345 Naira - 7 days",
            "Glo Data (SME) 3GB - 1,040 Naira - 7 days",
            "Glo Data (SME) 5GB - 1,730 Naira - 7 days",
            "Glo Data (SME) 1GB - 350 Naira - 14 days Night plan",
            "Glo Data (SME) 3GB - 1,040 Naira - 14 days Night plan",
            "Glo Data (SME) 5GB - 1,730 Naira - 14 days Night plan",
            "Glo Data (SME) 10GB - 3,460 Naira - 14 days Night plan",
            "Glo Data (SME) 200MB - 99 Naira - 14 days",
            "Glo Data (SME) 500MB - 250 Naira - 14 days",
            "Glo Data (SME) 500MB - 250 Naira - 30 days",
            "Glo Data (SME) 1GB - 495 Naira - 30 days",
            "Glo Data (SME) 2GB - 990 Naira - 30 days",
            "Glo Data (SME) 3GB - 1,485 Naira - 30 days",
            "Glo Data (SME) 3GB 5GB - 2,475 Naira - 30 days",
            "Glo Data (SME) 10GB - 4,950 Naira - 30 days"
        ]
    },
    "9mobile": {
        "9mobile Data": [
            "T2 83MB - 100 Naira - 1 day",
            "T2 150MB  + 100MB Night Data - 150 Naira - 1 day",
            "T2 650MB - 500 Naira - 3 days",
            "9mobile 2GB - 1,000 Naira - 30 Days",
            "T2 8.4GB - 4,000 Naira - 30 days",
            "T2 4.5GB - 2000 Naira - 30 Days",
            "T2 11.4GB - 5,000 Naira - 30 Days",
            "T2 6.2G - 3,000 Naira - 30 days",
            "T2 2.3GB - 1,200 Naira - 30 Days",
            "T2 40MB - 50 Naira - 1 day",
            "T2 5.2GB - 2,500 Naira - 30 days",
            "T2 N200 - 250MB Anytime Data Plan (7 Days)"
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
