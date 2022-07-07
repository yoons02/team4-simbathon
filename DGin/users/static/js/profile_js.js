const toggleBtn = document.querySelector(".navbar__toggleBtn");
const menu = document.querySelector(".navbar__menu");
const icons = document.querySelector(".navbar__icons");


// Nav Bar
toggleBtn.addEventListener("click", () => {
    menu.classList.toggle('active');
    icons.classList.toggle('active');
})
// Nav Bar


//Search Bar
var Tooltip = (function() {

    // Variables
  
    var $tooltip = $('[data-toggle="tooltip"]');
  
    function init() {
      $tooltip.tooltip();
    }
  
  
    // Events
    // Methods
  
    if ($tooltip.length) {
      init()
      f;
    }
  
  })();
// Search Bar