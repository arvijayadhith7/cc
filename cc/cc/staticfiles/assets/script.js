// desktop three bar link
function scrollToheader(sectionId) {
const section = document.getElementById(sectionId);
const offset = 50; // Adjust this value to scroll slightly lower
const sectionPosition = section.getBoundingClientRect().top + window.scrollY;

window.scrollTo({
    top: sectionPosition - offset,
    behavior: "smooth"
});
}

document.addEventListener("scroll", function() {
  const scrollBtn = document.querySelector(".scroll-to-top");
  // Show button after scrolling 300px, hide when at top
  if (window.scrollY > 300) {
      scrollBtn.classList.add("visible");
  } else {
      scrollBtn.classList.remove("visible");
  }
});

// Smooth scroll to top
document.querySelector(".scroll-to-top").addEventListener("click", function(e) {
  e.preventDefault();
  window.scrollTo({
      top: 0,
      behavior: "smooth"
  });
});

    function toggleMenu() {
        document.querySelector(".tabs").classList.toggle("active");
    }
    

   // Get references to the hamburger menu and navigation menu
const hamburgerMenu = document.getElementById('hamburger-menu');
const navMenu = document.getElementById('nav-menu');

// Function to check screen size and hide menu if necessary
function checkScreenSize() {
  if (window.innerWidth > 720) {
    // Hide the navigation menu and reset the hamburger icon
    navMenu.classList.remove('active');
    hamburgerMenu.classList.remove('active');
  }
}

// Toggle the active class on click
hamburgerMenu.addEventListener('click', (e) => {
  e.stopPropagation(); // Prevent the click from bubbling up to the document
  hamburgerMenu.classList.toggle('active');
  navMenu.classList.toggle('active');
});

// Close the menu when clicking outside
document.addEventListener('click', (e) => {
  if (!navMenu.contains(e.target) && !hamburgerMenu.contains(e.target)) {
    hamburgerMenu.classList.remove('active');
    navMenu.classList.remove('active');
  }
});

// Check screen size on window resize
window.addEventListener('resize', checkScreenSize);