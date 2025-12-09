// main.js — tiny behavior helpers for The Crocheted Crumb

// Mobile navigation toggle
const navToggle = document.querySelector(".nav-toggle");
const navList = document.querySelector(".nav-list");

if (navToggle && navList) {
  navToggle.addEventListener("click", () => {
    const isOpen = navList.classList.toggle("nav-list-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

// Dynamic year in footer
const yearSpanList = document.querySelectorAll("#year");
const currentYear = new Date().getFullYear();

yearSpanList.forEach((el) => {
  el.textContent = String(currentYear);
});
