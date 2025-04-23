document.addEventListener('DOMContentLoaded', function() {
  const navToggle = document.getElementById('nav-toggle');
  const sidebar = document.querySelector('.sidebar');
  const navLinks = document.querySelectorAll('.nav-item a');
  
  // Toggle mobile navigation
  navToggle.addEventListener('click', function() {
    sidebar.classList.toggle('active');
  });
  
  // Close navigation when clicking outside on mobile
  document.addEventListener('click', function(event) {
    const isClickInsideNav = sidebar.contains(event.target);
    const isClickOnToggle = navToggle.contains(event.target);
    
    if (!isClickInsideNav && !isClickOnToggle && sidebar.classList.contains('active')) {
      sidebar.classList.remove('active');
    }
  });
  
  // Set active nav item based on current page
  navLinks.forEach(link => {
    if (link.getAttribute('href') === getCurrentPage()) {
      link.parentElement.classList.add('active');
    } else {
      link.parentElement.classList.remove('active');
    }
  });
  
  // Helper function to get current page
  function getCurrentPage() {
    const path = window.location.pathname;
    const page = path.split('/').pop();
    return page || 'index.html';
  }
});