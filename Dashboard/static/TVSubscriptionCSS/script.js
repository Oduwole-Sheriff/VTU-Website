let tvImages = {
    'DSTV': "https://play-lh.googleusercontent.com/7qC9U2bMvcbgKWnxwfbEL805L1AcrgCKj9y7yO6vaqUYrwtZFGOj5wZp4dhR4rw77Ng=w526-h296-rw",
    'GOTV': "https://money.ke/wp-content/uploads/2024/12/gotv-supa-package-and-pricing.webp",
    'STARTIMES': "https://read.cardtonic.com/wp-content/smush-webp/2024/07/How-to-Renew-Your-Startime-Subscription-Online-in-2024@3x-100-scaled.jpg.webp",
    'SHOWMAX': "https://www.dstv.com/media/g4ulghp3/1099_showmax_to_lower_tiers_1920_x_1080_centered3.jpg"
};

let remoteClicked = false;
let currentImage = null;

const bouquetOptions = {
    'DSTV': [
        "DStv Padi N1,850",
        "DStv Yanga N2,565",
        "DStv Confam N4,615",
        "DStv Compact N7,900",
        "DStv Premium N18,400",
        "DStv Asia N6,200",
        "DStv Compact Plus N12,400",
        "DStv Premium-French N25,550",
        "DStv Premium-Asia N20,500",
        "DStv Confam + ExtraView N7,115",
        "DStv Yanga + ExtraView N5,065",
        "DStv Padi + ExtraView N4,350",
        "DStv Compact + Asia N14,100",
        "DStv Compact + Extra View N10,400",
        "DStv Compact + French Touch N10,200",
        "DStv Premium - Extra View N20,900",
        "DStv Compact Plus - Asia N18,600",
        "DStv Compact + French Touch + ExtraView N12,700",
        "DStv Compact + Asia + ExtraView N16,600",
        "DStv Compact Plus + French Plus N20,500",
        "DStv Compact Plus + French Touch N14,700",
        "DStv Compact Plus - Extra View N14,900",
        "DStv Compact Plus + FrenchPlus + Extra View N23,000",
        "DStv Compact + French Plus N16,000",
        "DStv Compact Plus + Asia + ExtraView N21,100",
        "DStv Premium + Asia + Extra View N23,000",
        "DStv Premium + French + Extra View N28,000",
        "DStv HDPVR Access Service N2,500",
        "DStv French Plus Add-on N8,100",
        "DStv Asian Add-on N6,200",
        "DStv French Touch Add-on N2,300",
        "ExtraView Access N2,500",
        "DStv French 11 N3,260"
    ],
    'GOTV': [
        "GOtv Lite N410",
        "GOtv Max N3,600",
        "GOtv Jolli N2,460",
        "GOtv Jinja N1,640",
        "GOtv Lite (3 Months) N1,080",
        "GOtv Lite (1 Year) N3,180"
    ],
    'STARTIMES': [
        "Nova - 900 Naira - 1 Month",
        "Basic - 1,700 Naira - 1 Month",
        "Smart - 2,200 Naira - 1 Month",
        "Classic - 2,500 Naira - 1 Month",
        "Super - 4,200 Naira - 1 Month",
        "Nova - 300 Naira - 1 Week",
        "Basic - 600 Naira - 1 Week",
        "Smart - 700 Naira - 1 Week",
        "Classic - 1200 Naira - 1 Week",
        "Super - 1,500 Naira - 1 Week",
        "Nova - 90 Naira - 1 Day",
        "Basic - 160 Naira - 1 Day",
        "Smart - 200 Naira - 1 Day",
        "Classic - 320 Naira - 1 Day",
        "Super - 400 Naira - 1 Day",
        "ewallet Amount"
    ],
    'SHOWMAX': [] // Showmax doesn't have bouquet options
};

// Add event listener to the remote control image
document.getElementById('remote-control').addEventListener('click', function() {
    // Toggle through TV images when remote is clicked
    let tvKeys = Object.keys(tvImages);
    let nextKeyIndex = tvKeys.indexOf(currentImage) + 1;
    if (nextKeyIndex >= tvKeys.length) nextKeyIndex = 0;

    currentImage = tvKeys[nextKeyIndex];
    document.getElementById('current-tv').innerHTML = `<img src="${tvImages[currentImage]}" alt="${currentImage}" id="${currentImage}">`;

    // Reset form and hide it if a new image is displayed
    document.getElementById('form-container').classList.remove('show');

    // Update the form fields immediately when the new TV service is displayed
    updateFormFields(currentImage);
});

// Add event listener to TV images for showing the form
document.getElementById('current-tv').addEventListener('click', function(e) {
    if (e.target.tagName === 'IMG') {
        // Show the form when any TV image is clicked
        document.getElementById('form-container').classList.add('show');
    }
});

// // Function to update form fields based on TV image
function updateFormFields(tvImage) {
    // Update the hidden 'tv_service' field with the current TV service
    document.getElementById('tv_service').value = tvImage;
    
    // Select all the fields you want to modify dynamically
    const fields = {
        'DSTV': { input: document.getElementById('smartcard-number-DSTV'), label: document.getElementById('smartcard-label-DSTV') },
        'GOTV': { input: document.getElementById('smartcard-number-GOTV'), label: document.getElementById('smartcard-label-GOTV') },
        'STARTIMES': { input: document.getElementById('smartcard-number-STARTIMES'), label: document.getElementById('smartcard-label-STARTIMES') },
        'bouquet': { input: document.getElementById('bouquet'), label: document.getElementById('bouquet-label') },
        'action': { input: document.getElementById('action'), label: document.getElementById('action-label') },
        'type': { input: document.getElementById('type'), label: document.getElementById('type-label') }
    };

    // Reset all form elements
    Object.values(fields).forEach(field => {
        field.input.style.display = 'none';
        field.input.removeAttribute('required');
        field.label.style.display = 'none';
    });

    // Now show the necessary fields
    if (tvImage === 'GOTV') {
        fields['GOTV'].label.style.display = 'block';
        fields['GOTV'].input.style.display = 'block';
        fields['GOTV'].input.setAttribute('required', 'true');
        fields['action'].label.style.display = 'block';
        fields['action'].input.style.display = 'block';
        fields['action'].input.setAttribute('required', 'true');
    } else if (tvImage === 'DSTV') {
        fields['DSTV'].label.style.display = 'block';
        fields['DSTV'].input.style.display = 'block';
        fields['DSTV'].input.setAttribute('required', 'true');
        fields['action'].label.style.display = 'block';
        fields['action'].input.style.display = 'block';
        fields['action'].input.setAttribute('required', 'true');
    } else if (tvImage === 'STARTIMES') {
        fields['STARTIMES'].label.style.display = 'block';
        fields['STARTIMES'].input.style.display = 'block';
        fields['STARTIMES'].input.setAttribute('required', 'true');
        fields['bouquet'].label.style.display = 'block';
        fields['bouquet'].input.style.display = 'block';
        fields['bouquet'].input.setAttribute('required', 'true');
        populateBouquetSelect(tvImage);
    } else if (tvImage === 'SHOWMAX') {
        fields['type'].label.style.display = 'block';
        fields['type'].input.style.display = 'block';
        fields['type'].input.setAttribute('required', 'true');

        let form = document.getElementById('tvForm');
        form.After(fields['type'].label, document.getElementById('phone-number'));
        form.After(fields['type'].input, document.getElementById('phone-number'));
    }
}

// Function to populate bouquet select options based on the selected TV service
function populateBouquetSelect(tvImage) {
    const bouquetSelect = document.getElementById('bouquet');
    const bouquets = bouquetOptions[tvImage];

    // Clear existing options (but keep the default one)
    bouquetSelect.innerHTML = '<option value="" disabled selected>Select a bouquet</option>';

    bouquets.forEach(function(bouquet) {
        let option = document.createElement('option');
        option.value = bouquet;
        option.textContent = bouquet;
        bouquetSelect.appendChild(option);
    });
}

// Show the bouquet field if the user selects "Change Bouquet"
document.getElementById('action').addEventListener('change', function() {
    const bouquetField = document.getElementById('bouquet');
    const bouquetLabel = document.getElementById('bouquet-label');
    if (this.value === 'change') {
        bouquetField.style.display = 'block';
        bouquetLabel.style.display = 'block';
        // Populate bouquet options for DSTV or GOTV
        const tvImage = currentImage;
        if (tvImage === 'DSTV' || tvImage === 'GOTV') {
            populateBouquetSelect(tvImage);
        }
    } else {
        bouquetField.style.display = 'none';
        bouquetLabel.style.display = 'none';
    }
});

// Add event listener to the bouquet field
document.getElementById('bouquet').addEventListener('change', function() {
    const selectedBouquet = this.value;

    // Check if a bouquet is selected
    if (selectedBouquet) {
        // Extract the amount from the bouquet (amount is the last part of the string after the last space)
        const amountMatch = selectedBouquet.match(/(\d[\d,]*)$/);
        if (amountMatch) {
            // Set the extracted amount into the 'amount' input field
            document.getElementById('amount').value = amountMatch[0].replace(/,/g, ''); // Remove commas if present
            // Disable the amount field after it is set
            document.getElementById('amount').disabled = true;
        }
    }

    // Check if a bouquet is selected
    if (selectedBouquet) {
        // Extract the amount from the bouquet (amount is the last part of the string after the last space)
        const amountMatch = selectedBouquet.match(/(\d{1,3}(?:,\d{3})*)(?=\s*Naira)/);
        if (amountMatch) {
            // Set the extracted amount into the 'amount' input field
            document.getElementById('amount').value = amountMatch[0].replace(/,/g, ''); // Remove commas if present
            // Disable the amount field after it is set
            document.getElementById('amount').disabled = true;
        }
    }
});

// Add event listener to the type field to auto-populate the amount field
document.getElementById('type').addEventListener('change', function() {
    const selectedType = this.value;
    const amountField = document.getElementById('amount');
    
    // Define the amounts for each type option
    const amounts = {
        "full": 2900,
        "mobile_only": 1450,
        "sports_full": 6300,
        "sports_mobile_only": 3200
    };

    // Check if a valid type is selected and set the amount
    if (selectedType in amounts) {
        // Set the amount in the amount field and disable the field
        amountField.value = amounts[selectedType];
        amountField.disabled = true; // Disable the field to prevent editing
    }
});


// Initialize first TV service (DSTV) by default
currentImage = 'DSTV';
document.getElementById('current-tv').innerHTML = `<img src="${tvImages[currentImage]}" alt="${currentImage}" id="${currentImage}">`;
updateFormFields(currentImage);