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
        "DStv Padi N4,400",
        "DStv Yanga N6,000",
        "Dstv Confam N11,000",
        "DStv  Compact N19,000",
        "DStv Premium N44,500",
        "DStv Compact Plus N30,000",
        "DStv Premium-French N69,000",
        "DStv Premium-Asia N50,500",
        "DStv Confam + ExtraView N17,000",
        "DStv Yanga + ExtraView N12,000",
        "DStv Padi + ExtraView N10,400",
        "DStv Compact + Extra View N25,000",
        "DStv Compact + French Touch N26,000",
        "DStv Premium + Extra View N50,500",
        "DStv Compact + French Touch + ExtraView N32,000",
        "DStv Compact Plus + French Plus N54,500",
        "DStv Compact Plus + French Touch N37,000",
        "DStv Compact Plus + Extra View N36,000",
        "DStv Compact Plus + FrenchPlus + Extra View N60,500",
        "DStv Compact + French Plus N43,500",
        "DStv Premium + French + Extra View N75,000",
        "DStv French Plus Add-on N24,500",
        "DStv Great Wall Standalone Bouquet N3,800",
        "DStv French Touch Add-on N7,000",
        "ExtraView Access N6,000",
        "DStv Yanga + Showmax N7,750",
        "DStv Great Wall Standalone Bouquet + Showmax N7,300",
        "DStv Compact Plus + Showmax N31,750",
        "Dstv Confam + Showmax N12,750",
        "DStv  Compact + Showmax N20,750",
        "DStv Padi + Showmax N7,900",
        "DStv Asia + Showmax N18,400",
        "DStv Premium + French + Showmax N69,000",
        "DStv Premium + Showmax N44,500",
        "DStv Indian N14,900",
        "DStv Premium East Africa and Indian N16530",
        "DStv FTA Plus N1,600",
        "DStv PREMIUM HD N39,000",
        "DStv Access N2000",
        "DStv Family",
        "DStv India Add-on N14,900",
        "DSTV MOBILE N790",
        "DStv Movie Bundle Add-on N3500",
        "DStv PVR Access Service N4000",
        "DStv Premium W/Afr + Showmax N50,500"
    ],
    'GOTV': [
        "GOtv Max N8,500",
        "GOtv Jolli N5,800",
        "GOtv Jinja N3,900",
        "GOtv Smallie - monthly N1900",
        "GOtv Smallie - quarterly N5,100",
        "GOtv Smallie - yearly N15,000",
        "GOtv Supa - monthly N11,400",
        "GOtv Supa Plus - monthly N16,800"
    ],
    'STARTIMES': [
        "Nova (Dish) - 2100 Naira - 1 Month",
        "Basic (Antenna) - 4,000 Naira - 1 Month",
        "Basic (Dish) - 5,100 Naira - 1 Month",
        "Classic (Antenna) - 6000 Naira - 1 Month",
        "Super (Dish) - 9,800 Naira - 1 Month",
        "Nova (Antenna) - 700 Naira - 1 Week",
        "Basic (Antenna) - 1400 Naira - 1 Week",
        "Basic (Dish) - 1,700 Naira - 1 Week",
        "Classic (Antenna) - 2000 Naira - 1 Week",
        "Super (Dish) - 3,300 Naira - 1 Week",
        "Chinese (Dish) - 21,000 Naira - 1 month",
        "Nova (Antenna) - 2,100 Naira - 1 Month",
        "Classic (Dish) - 2300 Naira - 1 Week",
        "Classic (Dish) - 7400 Naira - 1 Month",
        "Nova (Dish) - 700 Naira - 1 Week",
        "Super (Antenna) - 3,200 Naira - 1 Week",
        "Super (Antenna) - 9,500 Naira - 1 Month",
        "Classic (Dish) - 2500 Naira - 1 Week",
        "Global (Dish) - 21000 Naira - 1 Month",
        "Global (Dish) - 7000 Naira - 1Week",
        "Startimes SHS - 2,800 Naira - Weekly",
        "Startimes SHS - 4,620 Naira - Weekly",
        "Startimes SHS - 4,900 Naira - Weekly",
        "Startimes SHS - 9,100 Naira - Weekly",
        "Startimes SHS - 12,000 Naira - Monthly",
        "Startimes SHS - 19,800 Naira - Monthly",
        "Startimes SHS - 21,000 Naira - Monthly",
        "Startimes SHS - 39,000 Naira - Monthly"
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
    const amountField = document.getElementById('amountField');

    let amount = null;

    // Match "N2,565" or "- N850,000"
    let matchN = selectedBouquet.match(/N\s?([\d,]+)/i);
    let matchNaira = selectedBouquet.match(/([\d,]+)\s*Naira/i);
    let matchEnd = selectedBouquet.match(/(\d[\d,]*)$/);

    if (matchN) {
        amount = matchN[1];
    } else if (matchNaira) {
        amount = matchNaira[1];
    } else if (matchEnd) {
        amount = matchEnd[1];
    }

    if (amount) {
        // Remove all commas and non-digit characters
        const cleanAmount = amount.replace(/[^0-9.]/g, '');
        
        // Set both value and attribute
        amountField.value = cleanAmount;
        amountField.setAttribute('value', cleanAmount);
        amountField.readOnly = true;

        // Optional: trigger label float
        amountField.dispatchEvent(new Event('input'));
    } else {
        amountField.value = '';
        amountField.setAttribute('value', '');
        amountField.readOnly = false;
    }

    console.log("Amount field after update:", amountField.value);


    // Check if a bouquet is selected
    // if (selectedBouquet) {
    //     // Extract the amount from the bouquet (amount is the last part of the string after the last space)
    //     const amountMatch = selectedBouquet.match(/(\d{1,3}(?:,\d{3})*)(?=\s*Naira)/);
    //     if (amountMatch) {
    //         // Set the extracted amount into the 'amount' input field
    //         document.getElementById('amount').value = amountMatch[0].replace(/,/g, ''); // Remove commas if present
    //         // Disable the amount field after it is set
    //         document.getElementById('amount').disabled = true;
    //     }
    // }
});

// Add event listener to the type field to auto-populate the amount field
document.getElementById('type').addEventListener('change', function() {
    const selectedType = this.value;
    const amountField = document.getElementById('amountField');
    
    // Map of variation_code to amount
    const amounts = {
        "full": 4500,
        "mobile_only": 2000,
        "full_sports_mobile_only": 6500,
        "sports_mobile_only": 4500,
        "full_3": 9000,
        "mobile_only_3": 4000,
        "sports_mobile_only_3": 13500,
        "sports-only-1": 3600,
        "sports-only-3": 7200,
        "full-sports-mobile-only-3": 19500,
        "mobile-only-6": 7800,
        "full-only-6": 17550,
        "full-sports-mobile-only-6": 39000,
        "sports-mobile-only-6": 27000,
        "sports-only-6": 14040
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