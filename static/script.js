const menuToggle = document.getElementById("menu-toggle");
const navbar = document.querySelector(" .navbar");
menuToggle.addEventListener("click", () => {
    navbar.classList.toggle("active");
});
// scroll-triggerd animation using IntersectionObserver
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
    if (entry.isIntersecting) { 
        entry.target.classList.add('visible');
    } else {
        entry.target.classList.remove('visible'); // removes when leaving
    }
  });
}, {
  threshold: 0.1
});
// Apply observer to all sections with fade-in effect
document.querySelectorAll('.fade-in-section').forEach(section => {
    observer.observe(section);
}); 
// Flip Items with Staggered Animation
const flipItems = document.querySelectorAll('.flip-item');
const flipObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const items = entry.target.closest('section')?.querySelectorAll('.flip-item') || [entry.target];
      items.forEach((item, index) => {
        setTimeout(() => {
          item.classList.add("visible");
        }, index * 200); // Adjust this delay (in ms) for slower or faster stagger
      });
    } else {
      const items = entry.target.closest('section')?.querySelectorAll('.flip-item') || [entry.target];
      items.forEach(item => {
        item.classList.remove("visible"); // Remove when out of view
      });
    }
  });
}, {
  threshold: 0.1
});
// Observe flip-item sections
flipItems.forEach(element => {
  flipObserver.observe(element);
});


