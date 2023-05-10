// Set the interval duration (in milliseconds)
var intervalDuration = 1000; // 3 seconds

// Get all the slide elements
var slides = document.querySelectorAll('.ci');

// Define a function to show the next slide
function showNextSlide() {
    // Find the currently active slide
    var activeSlide = document.querySelector('.ci.active');

    // Find the next slide
    var nextSlide = activeSlide.nextElementSibling;
    if (!nextSlide) {
        // If there is no next slide, go back to the first slide
        nextSlide = slides[0];
    }

    // Remove the active class from the current slide
    activeSlide.classList.remove('active');

    // Add the active class to the next slide
    nextSlide.classList.add('active');
}

// Start the slideshow
setInterval(showNextSlide, intervalDuration);
