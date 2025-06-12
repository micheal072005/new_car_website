//  messageContainer -->
setTimeout(function() {
    const messageContainer = document.querySelector('.message');
    if (messageContainer) {
      messageContainer.style.display = 'none';
    }
  }, 3000); 
  

//  Toggle Password  Visibility for register form
function togglePassword(inputId, eyeOpenId, eyeSlashId) {
    let passwordInput = document.getElementById(inputId);
    let eyeOpen = document.getElementById(eyeOpenId);
    let eyeSlash = document.getElementById(eyeSlashId);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeOpen.classList.add("hidden");
        eyeSlash.classList.remove("hidden");
    } else {
        passwordInput.type = "password";
        eyeOpen.classList.remove("hidden");
        eyeSlash.classList.add("hidden");
    }
}


// Mobile menu toggle
const menuBtn = document.getElementById("menu-btn");
const menu = document.getElementById("menu");
const menuIcon = document.getElementById("menu-icon");
const closeIcon = document.getElementById("close-icon");

// Toggle menu on button click
menuBtn.addEventListener("click", (event) => {
    event.stopPropagation(); // Prevent event from triggering document click
    if (menu.classList.contains("hidden")) {
        openMenu();
    } else {
        closeMenu();
    }
});


// Close menu if clicking anywhere outside of it
document.addEventListener("click", (event) => {
    if (!menu.contains(event.target) && !menuBtn.contains(event.target)) {
        if (!menu.classList.contains("hidden")) {
            closeMenu();
        }
    }
});

// Open and close menu functions
function openMenu() {
    menu.classList.remove("hidden");
    menu.classList.add("animate-slide-in");
    menuIcon.classList.add("hidden");
    setTimeout(() => {
        closeIcon.classList.remove("hidden");
    }, 300);
}

function closeMenu() {
    menu.classList.add("animate-slide-out");
    setTimeout(() => {
        menu.classList.remove("animate-slide-out");
        menu.classList.add("hidden");
        setTimeout(() => {
            menuIcon.classList.remove("hidden");
        }, 300);
        closeIcon.classList.add("hidden");
    }, 300); // Match animation duration
}

// Swiper slider
document.addEventListener("DOMContentLoaded", function () {
    const swiper = new Swiper('.swiper', {
        loop: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });
});


// AOS animations
document.addEventListener("DOMContentLoaded", function () {
    AOS.init({
        once: false,  // Ensures animation happens every time an element enters the viewport
        duration: 1000, // Adjust animation duration as needed
        offset: 100, // Adjust how early animation starts when scrolling
    });

    // Listen for scroll and refresh AOS when elements come into view
    window.addEventListener("scroll", function () {
        AOS.refresh();
    });
});


// Confirm delete car
let deleteUrl = "";

function openDialog(itemId, action) {
    deleteUrl = `/${action}/${itemId}/`;
    document.getElementById("myDialog").showModal();
}

function closeDialog() {
    document.getElementById("myDialog").close();
}

document.getElementById("confirmDeleteBtn").addEventListener("click", function () {
    window.location.href = deleteUrl;
});




