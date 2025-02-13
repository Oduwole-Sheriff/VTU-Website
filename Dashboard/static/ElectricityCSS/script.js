document.addEventListener("DOMContentLoaded", function () {
    const prevButton = document.querySelector('.prev-btn');
    const nextButton = document.querySelector('.next-btn');
    const carouselImages = document.querySelector('.carousel-images');
    const images = document.querySelectorAll('.carousel-image');
    const dots = document.querySelectorAll('.dot');
    const totalImages = images.length;
    const formContainer = document.querySelector('.form-container');
    const imageNameElement = document.querySelector('.image-name');
    const form = document.querySelector('#form');
    const serviceID = document.querySelector('#serviceID');
  
    let currentIndex = 0;
    let activeDot = null; // Track the active dot
  
    // Function to update the carousel and dots
    function updateCarousel() {
      // Move the carousel images
      carouselImages.style.transform = `translateX(-${currentIndex * (images[0].clientWidth + 20)}px)`;
  
      // Update active class for images
      images.forEach((image, index) => {
        if (index === currentIndex) {
          image.classList.add('active');
        } else {
          image.classList.remove('active');
        }
      });
  
      // Update active class for dots
      dots.forEach((dot, index) => {
        if (index === currentIndex) {
          dot.classList.add('active');
        } else {
          dot.classList.remove('active');
        }
      });
    }
  
    // Auto slide every 3 seconds
    let autoSlide = setInterval(() => {
      nextButton.click();
    }, 3000);
  
    // Event listener for previous button
    prevButton.addEventListener('click', () => {
      if (currentIndex > 0) {
        currentIndex--;
      } else {
        currentIndex = totalImages - 1;
      }
      updateCarousel();
      resetAutoSlide();
    });
  
    // Event listener for next button
    nextButton.addEventListener('click', () => {
      if (currentIndex < totalImages - 1) {
        currentIndex++;
      } else {
        currentIndex = 0; // Now move from the last to the first image, seamlessly
      }
      updateCarousel();
      resetAutoSlide();
    });
  
    // Reset auto-slide when user manually changes the image
    function resetAutoSlide() {
      clearInterval(autoSlide);
      autoSlide = setInterval(() => {
        nextButton.click();
      }, 3000);
    }
  
    // Event listener for dot click
    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        currentIndex = index;
        updateCarousel();
        resetAutoSlide();
      });
    });
  
    // Show form when image is clicked
    images.forEach((image) => {
      image.addEventListener('click', () => {
    
        console.log('Image clicked: ' + image.alt); // Debugging line
    
        // Display the form
        formContainer.classList.add('show');
        
        // Set the name of the image as the form header
        imageNameElement.textContent = image.alt;
    
        // Set the ID of the clicked image to the Electricity input field
        serviceID.value = image.id;
    
      });
    });  
  
    // Initialize carousel
    updateCarousel();
  });