function showForm(provider, selectedSquare) {
    // Display the form container
    const formContainer = document.getElementById("form-container");
    const networkInput = document.getElementById("network");
    const providerName = document.querySelector(".formHeading h2");

    // Remove "selected" class from all squares
    const allSquares = document.querySelectorAll('.square');
    allSquares.forEach(square => square.classList.remove('selected'));

    // Add "selected" class to the clicked square
    selectedSquare.classList.add('selected');

    // Set the provider name in the form
    providerName.textContent = provider + " Airtime TopUp";

    // Set the network value in the input
    networkInput.value = provider;

    // Show the form container
    formContainer.style.display = "block";
}