// Dark mode toggle + persistence
document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("themeToggle");
    if (!toggleBtn) return;

    // Load saved theme preference
    const savedMode = localStorage.getItem("tn_theme"); // tn = trusted notifications
    if (savedMode === "dark") {
        document.body.classList.add("dark-mode");
        toggleBtn.textContent = "☀️ Light Mode";
    } else {
        toggleBtn.textContent = "🌙 Dark Mode";
    }

    toggleBtn.addEventListener("click", function () {
        const isDark = document.body.classList.toggle("dark-mode");
        if (isDark) {
            localStorage.setItem("tn_theme", "dark");
            toggleBtn.textContent = "☀️ Light Mode";
        } else {
            localStorage.setItem("tn_theme", "light");
            toggleBtn.textContent = "🌙 Dark Mode";
        }
    });
});
