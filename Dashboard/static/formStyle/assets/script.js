// Select elements
const circles = document.querySelectorAll('.circle');
const modal = document.getElementById('modal');
const modalTitle = document.getElementById('modalTitle');
const modalFormContainer = document.getElementById('modalFormContainer');
const closeModal = document.getElementById('closeModal');

// Circle click event
circles.forEach((circle, index) => {
    circle.addEventListener('click', () => {
        openModal(index + 1); // Pass circle number to modal
    });
});

// Open modal with corresponding form based on circle clicked
function openModal(circleNumber) {
    modal.style.display = 'flex'; // Ensure modal uses flexbox to center it

    // Set modal title based on circle number
    modalTitle.textContent = `Form for Circle ${circleNumber}`;

    // Hide all forms initially
    const forms = document.querySelectorAll('form');
    forms.forEach(form => form.classList.remove('active'));

    // Show the selected form based on circle number
    const selectedForm = document.getElementById(`form${circleNumber}`);
    selectedForm.classList.add('active');
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
