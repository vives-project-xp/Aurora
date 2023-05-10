// Set the interval duration (in milliseconds)
var intervalDuration = 5000; // 5 seconds

// Get all the slide elements
var slides = document.querySelectorAll('.ci');

// Define a function to show the next slide
function showNextSlide() {
    // Find the currently active slide
    var activeSlide = document.querySelector('.ci.active');

    // Find the index of the active slide
    var activeIndex = Array.from(slides).indexOf(activeSlide);

    // Calculate the index of the next slide
    var nextIndex = (activeIndex + 1) % slides.length;

    // Remove the active class from the current slide
    activeSlide.classList.remove('active');

    // Add the active class to the next slide
    slides[nextIndex].classList.add('active');
}

// Start the slideshow
setInterval(showNextSlide, intervalDuration);

