// Select elements
const circles = document.querySelectorAll('.circle');
const modal = document.getElementById('modal');
const modalTitle = document.getElementById('modalTitle');
const closeModal = document.getElementById('closeModal');
const nextBtn1 = document.getElementById('nextBtn1');
const nextBtn2 = document.getElementById('nextBtn2');
const prevBtn1 = document.getElementById('prevBtn1');
const prevBtn2 = document.getElementById('prevBtn2');
const progressBar = document.getElementById('progress');
const dataPlanSelect = document.getElementById('dataPlanSelect'); // Changed from dataTypeSelect
const amountInput = document.querySelector('input[name="amount"]'); // Amount input field

// Store user input
let userData = {};

// Circle click event
circles.forEach((circle, index) => {
    circle.addEventListener('click', () => {
        openModal(index); // Pass circle index to modal
    });
});

// Open modal with corresponding form based on circle selection
function openModal(circleIndex) {
    modal.style.display = 'flex'; // Ensure modal uses flexbox to center it
    const circleNames = ['Airtel', 'MTN', '9Mobile', 'Glo'];
    modalTitle.textContent = `BigSheriffData for ${circleNames[circleIndex]}`;

    // Clear existing options before adding new ones
    dataPlanSelect.innerHTML = '<option value="">------</option>'; // Reset select

    // Set the select options dynamically based on the circle clicked
    switch (circleIndex) {
        case 0: // Airtel
            // Add Airtel-specific options dynamically
            const airtelOptions = [
                { value: '216', label: '100.0MB     CORPORATE GIFTING = ₦ 27.5  --- 7 days' },
                { value: '334', label: '250.0MB     AWOOF GIFTING = ₦  68.0  --- 14 days' },
                { value: '313', label: '100.0MB     AWOOF GIFTING = ₦  70.0  --- 1 day' },
                { value: '217', label: '300.0MB     CORPORATE GIFTING = ₦  82.5  --- 7 days' },
                { value: '301', label: '100.0MB     GIFTING = ₦  88.0  --- 1 day' },
                { value: '302', label: '450.0MB     GIFTING = ₦  105.6  ---1 day' },
                { value: '314', label: '300.0MB     AWOOF GIFTING = ₦  120.0  --- 2 days' },
                { value: '212', label: '500.0MB     CORPORATE GIFTING = ₦  137.5  --- 30 days' },
                { value: '333', label: '500.0MB     AWOOF GIFTING = ₦  138.0  ---- 14 days' },
                { value: '303', label: '200.0MB     GIFTING = ₦  176.0  ---1 day' },
                { value: '319', label: '1.0GB     AWOOF GIFTING = ₦  220.0  --- 2 days' },
                { value: '325', label: '1.0GB     AWOOF GIFTING = ₦  250.0  --- 7 days' },
                { value: '213', label: '1.0GB     CORPORATE GIFTING = ₦  275.0  --- 30 days' },
                { value: '300', label: '1.0GB     GIFTING = ₦  308.0  --- 1 day' },
                { value: '320', label: '2.0GB     AWOOF GIFTING = ₦  320.0  --- 2 days' },
                { value: '332', label: '1.5GB     AWOOF GIFTING = ₦  338.0  ---- 7 days' },
                { value: '126', label: '2.0GB     GIFTING = ₦  440.0  --- 2 day' },
                { value: '125', label: '1.0GB     GIFTING = ₦  440.0  --- 7 day' },
                { value: '130', label: '750.0MB     GIFTING = ₦  440.0  --- 7 days' },
                { value: '331', label: '2.0GB     AWOOF GIFTING = ₦  516.0  --- 14 days' },
                { value: '315', label: '3.0GB     AWOOF GIFTING = ₦  520.0  --- 7 days' },
                { value: '214', label: '2.0GB     CORPORATE GIFTING = ₦  550.0  --- 30 days' },
                { value: '132', label: '1.2GB     GIFTING = ₦  880.0  --- 30 days' },
                { value: '316', label: '4.0GB     AWOOF GIFTING = ₦  1020.0  --- 30 days' },
                { value: '131', label: '1.5GB     GIFTING = ₦  1056.0  --- 30 days' },
                { value: '329', label: '5.0GB     AWOOF GIFTING = ₦  1180.0  --- 14 days' },
                { value: '129', label: '6000.0MB     GIFTING = ₦  1320.0  --- 7 days' },
                { value: '133', label: '3.0GB     GIFTING = ₦  1320.0  --- 30 days' },
                { value: '215', label: '5.0GB     CORPORATE GIFTING = ₦  1375.0  --- 30 days' },
                { value: '330', label: '6.0GB     AWOOF GIFTING = ₦  1638.0  ---30 days' },
                { value: '134', label: '4.5GB     GIFTING = ₦  1760.0  --- 30 days' },
                { value: '317', label: '10.0GB     AWOOF GIFTING = ₦  2020.0  --- 30 days' },
                { value: '135', label: '6.0GB     GIFTING = ₦  2200.0  --- 30 days' },
                { value: '136', label: '10.0GB     GIFTING = ₦  2640.0  --- 30 days' },
                { value: '231', label: '10.0GB     CORPORATE GIFTING = ₦  2750.0  --- 30 days' },
                { value: '318', label: '15.0GB     AWOOF GIFTING = ₦  3020.0  --- 30 days' },
                { value: '138', label: '15.0GB     GIFTING = ₦  3520.0  --- 30 days' },
                { value: '328', label: '20.0GB     AWOOF GIFTING = ₦  4000.0  ---- 30 days' },
                { value: '232', label: '15.0GB     CORPORATE GIFTING = ₦  4125.0  --- 30 days' },
                { value: '137', label: '18.0GB     GIFTING = ₦  4400.0  --- 30 days' },
                { value: '299', label: '30.0GB     GIFTING = ₦  4400.0  --- 7 days Unltd Ultra Router' },
                { value: '233', label: '20.0GB     CORPORATE GIFTING = ₦  5500.0  --- 30 days' },
                { value: '326', label: '40.0GB     AWOOF GIFTING = ₦  7000.0  --- 30 days' },
                { value: '298', label: '30.0GB     GIFTING = ₦  7040.0  ---30 days' },
                { value: '139', label: '40.0GB     GIFTING = ₦  8800.0  --- 30 days' },
                { value: '140', label: '75.0GB     GIFTING = ₦  13200.0  --- 30 days' },
                { value: '141', label: '120.0GB     GIFTING = ₦  17600.0  --- 30 days' }
            ];

            airtelOptions.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = option.label; // Set the label as the option text
                dataPlanSelect.appendChild(optionElement);
            });

            // Add an event listener to update the amount field and disable it when a user selects an option
            dataPlanSelect.addEventListener('change', function () {
                const selectedOption = dataPlanSelect.options[dataPlanSelect.selectedIndex];
                const amount = selectedOption.textContent.split(' = ')[1].split(' --- ')[0]; // Extract amount from the option text

                // Update the amount input field with the selected amount
                amountInput.value = amount.trim();

                // Disable the amount input field after the user selects an option
                amountInput.disabled = true;
            });

            break;
        case 1: // MTN
            // Same logic as in your original code for MTN
            const mtnOptions = [
                { value: '234', label: '40.0MB GIFTING = ₦ 49.0 --- 1 day' },
                { value: '112', label: '100.0MB GIFTING = ₦ 96.0 --- 1 day' },
                { value: '238', label: '200.0MB GIFTING = ₦ 192.0 --- 2 days' },
                { value: '294', label: '1.0GB GIFTING = ₦ 285.0 --- 1 day' },
                { value: '336', label: '750.0MB GIFTING = ₦ 289.0 --- 1 day' },
                { value: '335', label: '2.0GB GIFTING = ₦ 480.0 --- 2 days' },
                { value: '239', label: '2.5GB GIFTING = ₦ 576.0 --- 2 days' },
                { value: '343', label: '1.2GB GIFTING = ₦ 960.0 --- 30 days' },
                { value: '338', label: '1.5GB GIFTING = ₦ 960.0 --- 7 days' }
            ];

            mtnOptions.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = option.label; // Set the label as the option text
                dataPlanSelect.appendChild(optionElement);
            });

            // Add an event listener to update the amount field and disable it when a user selects an option
            dataPlanSelect.addEventListener('change', function () {
                const selectedOption = dataPlanSelect.options[dataPlanSelect.selectedIndex];
                const amount = selectedOption.textContent.split(' = ')[1].split(' --- ')[0]; // Extract amount from the option text

                // Update the amount input field with the selected amount
                amountInput.value = amount.trim();

                // Disable the amount input field after the user selects an option
                amountInput.disabled = true;
            });

            break;
        case 2: // 9Mobile
            const nineMobileOptions = [
                { value: '117', label: '25.0MB     GIFTING = ₦  44.0  --- 1 day' },
                { value: '118', label: '100.0MB     GIFTING = ₦  84.0  --- 1 day' },
                { value: '275', label: '500.0MB     CORPORATE GIFTING = ₦  85.0  --- 30 days' },
                { value: '122', label: '250.0MB     GIFTING = ₦  168.0  --- 7 days' },
                { value: '119', label: '650.0MB     GIFTING = ₦  168.0  --- 1 day' },
                { value: '272', label: '1.0GB     CORPORATE GIFTING = ₦  170.0  --- 30 days' },
                { value: '120', label: '1.0GB     GIFTING = ₦  243.0  --- 1 day' },
                { value: '273', label: '1.5GB     CORPORATE GIFTING = ₦  255.0  --- 30 days' },
                { value: '241', label: '1.0GB     SME = ₦  300.0  --- 30 days' },
                { value: '274', label: '2.0GB     CORPORATE GIFTING = ₦  340.0  --- 30 days' },
                { value: '121', label: '2000.0MB     GIFTING = ₦  410.0  --- 1 day' },
                { value: '123', label: '500.0MB     GIFTING = ₦  410.0  --- 30 days' },
                { value: '276', label: '2.5GB     CORPORATE GIFTING = ₦  425.0  --- 30 days' },
                { value: '243', label: '1.5GB     SME = ₦  450.0  --- 30 days' },
                { value: '277', label: '3.0GB     CORPORATE GIFTING = ₦  510.0  --- 30 days' },
                { value: '242', label: '2.0GB     SME = ₦  600.0  --- 30 days' },
                { value: '278', label: '4.0GB     CORPORATE GIFTING = ₦  680.0  --- 30 days' },
                { value: '279', label: '4.5GB     CORPORATE GIFTING = ₦  765.0  --- 30 days' },
                { value: '36', label: '1.5GB     GIFTING = ₦  810.0  ---30 days' },
                { value: '295', label: '5.0GB     CORPORATE GIFTING = ₦  850.0  --- 30 days' },
                { value: '244', label: '3.0GB     SME = ₦  900.0  --- 30 days' },
                { value: '33', label: '2.0GB     GIFTING = ₦  972.0  --- 30 days' },
                { value: '247', label: '3.5GB     SME = ₦  1050.0  --- 30 days' },
                { value: '245', label: '4.0GB     SME = ₦  1200.0  --- 30 days' },
                { value: '246', label: '4.5GB     SME = ₦  1350.0  --- 30 days' },
                { value: '280', label: '10.0GB     CORPORATE GIFTING = ₦  1350.0  --- 30 days' },
                { value: '248', label: '5.0GB     SME = ₦  1500.0  --- 30 days' },
                { value: '15', label: '4.5GB     GIFTING = ₦  1620.0  ---30 days' },
                { value: '281', label: '15.0GB     CORPORATE GIFTING = ₦  2025.0  ...30days' },
                { value: '282', label: '20.0GB     CORPORATE GIFTING = ₦  2700.0  ...30days' },
                { value: '249', label: '10.0GB     SME = ₦  3000.0  --- 30 days' },
                { value: '14', label: '11.0GB     GIFTING = ₦  3240.0  --- 30 days' },
                { value: '13', label: '15.0GB     GIFTING = ₦  4050.0  ---30 days' },
                { value: '283', label: '30.0GB     CORPORATE GIFTING = ₦  4050.0  ...30days' },
                { value: '286', label: '50.0GB     CORPORATE GIFTING = ₦  6750.0  --- 30 days' },
                { value: '142', label: '40.0GB     GIFTING = ₦  8100.0  --- 30 days' },
                { value: '256', label: '40.0GB     SME = ₦  9100.0  --- 30 days' },
                { value: '284', label: '75.0GB     CORPORATE GIFTING = ₦  10125.0  ...30days' },
                { value: '58', label: '75.0GB     GIFTING = ₦  12150.0  --- 30 days' },
                { value: '285', label: '100.0GB     CORPORATE GIFTING = ₦  13500.0  --- 30 days' }
            ];

            // Add 9Mobile-specific options to the dropdown dynamically
            nineMobileOptions.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = option.label; // Set the label as the option text
                dataPlanSelect.appendChild(optionElement);
            });

            // Add an event listener to update the amount field and disable it when a user selects an option
            dataPlanSelect.addEventListener('change', function () {
                const selectedOption = dataPlanSelect.options[dataPlanSelect.selectedIndex];
                const amount = selectedOption.textContent.split(' = ')[1].split(' --- ')[0]; // Extract amount from the option text

                // Update the amount input field with the selected amount
                amountInput.value = amount.trim();

                // Disable the amount input field after the user selects an option
                amountInput.disabled = true;
            });
        case 3: // Glo
            const gloOptions = [
                { value: '301', label: '100.0MB GIFTING = ₦ 70.0 --- 1 day' },
                { value: '303', label: '250.0MB GIFTING = ₦ 150.0 --- 2 days' },
                { value: '305', label: '500.0MB GIFTING = ₦ 250.0 --- 7 days' },
                { value: '310', label: '1.0GB GIFTING = ₦ 450.0 --- 7 days' },
                { value: '315', label: '1.5GB GIFTING = ₦ 600.0 --- 7 days' },
                { value: '320', label: '2.0GB GIFTING = ₦ 800.0 --- 30 days' },
                { value: '330', label: '3.0GB GIFTING = ₦ 1000.0 --- 30 days' },
                { value: '340', label: '5.0GB GIFTING = ₦ 1500.0 --- 30 days' },
                { value: '350', label: '10.0GB GIFTING = ₦ 3000.0 --- 30 days' },
                { value: '360', label: '20.0GB GIFTING = ₦ 5000.0 --- 30 days' },
                { value: '370', label: '30.0GB GIFTING = ₦ 7000.0 --- 30 days' },
                { value: '380', label: '50.0GB GIFTING = ₦ 10000.0 --- 30 days' }
            ];

            // Add Glo-specific options to the dropdown dynamically
            gloOptions.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = option.label; // Set the label as the option text
                dataPlanSelect.appendChild(optionElement);
            });

            // Add an event listener to update the amount field and disable it when a user selects an option
            dataPlanSelect.addEventListener('change', function () {
                const selectedOption = dataPlanSelect.options[dataPlanSelect.selectedIndex];
                const amount = selectedOption.textContent.split(' = ')[1].split(' --- ')[0]; // Extract amount from the option text

                // Update the amount input field with the selected amount
                amountInput.value = amount.trim();

                // Disable the amount input field after the user selects an option
                amountInput.disabled = true;
            });
            break;

    }

    // Show the first form and update progress bar
    document.getElementById('form1').classList.add('active');
    document.getElementById('step2').classList.remove('active');
    document.getElementById('step3').classList.remove('active');
    progressBar.style.width = '33.33%'; // Update to step 1
}

// Close modal when close button is clicked
closeModal.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Close modal if clicked outside of the modal content
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

// Step 1: Go to Step 2 (Review Data)
nextBtn1.addEventListener('click', () => {
    // Capture data from Form 1
    userData.dataPlan = dataPlanSelect.options[dataPlanSelect.selectedIndex].text; // Store label text as dataPlan
    userData.mobileNumber = document.querySelector('input[name="mobile_number"]').value;
    userData.amount = document.querySelector('input[name="amount"]').value;

    // Move to Step 2
    document.getElementById('form1').classList.remove('active');
    document.getElementById('step2').classList.add('active');
    document.getElementById('step3').classList.remove('active');

    // Display the review data
    document.getElementById('reviewDataPlan').textContent = userData.dataPlan; // Updated to dataPlan
    document.getElementById('reviewMobileNumber').textContent = userData.mobileNumber;
    document.getElementById('reviewAmount').textContent = userData.amount;

    // Update progress bar
    progressBar.style.width = '66.66%'; // Move to second step
});

// Step 2: Go to Step 3 (Receipt)
nextBtn2.addEventListener('click', () => {
    // Move to Step 3 (Receipt Preview)
    document.getElementById('step2').classList.remove('active');
    document.getElementById('step3').classList.add('active');

    // Display the receipt with all user input
    document.getElementById('receiptDataPlan').textContent = userData.dataPlan; // Updated to dataPlan
    document.getElementById('receiptMobileNumber').textContent = userData.mobileNumber;
    document.getElementById('receiptAmount').textContent = userData.amount;

    // Update progress bar
    progressBar.style.width = '100%'; // Move to third step
});

// Step 1: Go back to Step 1 from Step 2
prevBtn1.addEventListener('click', () => {
    document.getElementById('step2').classList.remove('active');
    document.getElementById('form1').classList.add('active');
    progressBar.style.width = '33.33%'; // Reset to first step
});

// Step 2: Go back to Step 2 from Step 3
prevBtn2.addEventListener('click', () => {
    document.getElementById('step3').classList.remove('active');
    document.getElementById('step2').classList.add('active');
    progressBar.style.width = '66.66%'; // Reset to second step
});

// Submit final data
document.querySelector('button[type="submit"]').addEventListener('click', () => {
    alert('Form submitted successfully!');
    modal.style.display = 'none'; // Close modal on submit
});
