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

// Store user input
let userData = {};

// Circle click event
circles.forEach((circle, index) => {
    circle.addEventListener('click', () => {
        openModal(index + 1); // Pass circle number to modal
    });
});


// Open modal with corresponding form based on circle number
function openModal(circleNumber) {
    modal.style.display = 'flex'; // Ensure modal uses flexbox to center it
    modalTitle.textContent = `Form for Circle ${circleNumber}`;

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
    userData.name = document.getElementById('name1').value;
    userData.email = document.getElementById('email1').value;

    // Move to Step 2
    document.getElementById('form1').classList.remove('active');
    document.getElementById('step2').classList.add('active');
    document.getElementById('step3').classList.remove('active');

    // Display the review data
    document.getElementById('reviewName').textContent = userData.name;
    document.getElementById('reviewEmail').textContent = userData.email;

    // Update progress bar
    progressBar.style.width = '66.66%'; // Move to second step
});

// Step 2: Go to Step 3 (Receipt)
nextBtn2.addEventListener('click', () => {
    // Move to Step 3 (Receipt Preview)
    document.getElementById('step2').classList.remove('active');
    document.getElementById('step3').classList.add('active');

    // Display the receipt with all user input
    document.getElementById('receiptName').textContent = userData.name;
    document.getElementById('receiptEmail').textContent = userData.email;
    document.getElementById('receiptAddress').textContent = userData.address || 'N/A';
    document.getElementById('receiptPhone').textContent = userData.phone || 'N/A';
    document.getElementById('receiptMessage').textContent = userData.message || 'N/A';

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
