function showForm(provider, selectedSquare) {
    // Display the form container
    const formContainer = document.getElementById("form-container");
    const networkNameInput = document.getElementById("network-name");
    const networkInput = document.getElementById("network"); // Hidden input to store the numeric value
    const providerName = document.querySelector(".formHeading h2");

    // Remove "selected" class from all squares
    const allSquares = document.querySelectorAll('.square');
    allSquares.forEach(square => square.classList.remove('selected'));

    // Add "selected" class to the clicked square
    selectedSquare.classList.add('selected');

    // Set the provider name in the form
    const networkNames = {
        1: "MTN",
        2: "GLO",
        3: "9MOBILE",
        4: "AIRTEL"
    };

    const networkName = networkNames[provider];  // Get the name corresponding to the network ID
    providerName.textContent = `${networkName} Airtime TopUp`;  // Display the name in the header

    // Set the network name in the visible input field
    networkNameInput.value = networkName; // Show the network name in the 'Network' field

    // Set the network value (numeric) in the hidden input field
    networkInput.value = provider; // This holds the numeric value for backend processing

    // Show the form container
    formContainer.style.display = "block";
}
