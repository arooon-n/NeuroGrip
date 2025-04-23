document.addEventListener('DOMContentLoaded', function() {
  const themeSwitch = document.getElementById('theme-switch');
  const themeLabel = document.querySelector('.theme-label');
  
  // Check for saved theme preference or use preferred color scheme
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  // Apply theme based on saved preference or system preference
  if (savedTheme === 'dark' || (savedTheme === null && prefersDark)) {
    document.body.classList.add('dark-theme');
    themeSwitch.checked = true;
    themeLabel.textContent = 'Light Mode';
  } else {
    document.body.classList.remove('dark-theme');
    themeSwitch.checked = false;
    themeLabel.textContent = 'Dark Mode';
  }
  
  // Toggle theme on switch change
  themeSwitch.addEventListener('change', function() {
    if (this.checked) {
      document.body.classList.add('dark-theme');
      localStorage.setItem('theme', 'dark');
      themeLabel.textContent = 'Light Mode';
    } else {
      document.body.classList.remove('dark-theme');
      localStorage.setItem('theme', 'light');
      themeLabel.textContent = 'Dark Mode';
    }
  });
});