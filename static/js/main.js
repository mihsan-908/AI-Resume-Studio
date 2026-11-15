// Global script for ResumeAI
document.addEventListener("DOMContentLoaded", function () {
    // Mobile navigation toggle
    const toggleBtn = document.getElementById("mobileMenuToggle");
    const sidebar = document.getElementById("sidebar");
    const backdrop = document.getElementById("sidebarBackdrop");

    if (toggleBtn && sidebar && backdrop) {
        toggleBtn.addEventListener("click", function () {
            sidebar.classList.toggle("open");
            backdrop.classList.toggle("active");
        });

        backdrop.addEventListener("click", function () {
            sidebar.classList.remove("open");
            backdrop.classList.remove("active");
        });
    }
});

// Toast notification helper
function showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `alert alert-${type}`;
    toast.style.position = "fixed";
    toast.style.bottom = "24px";
    toast.style.right = "24px";
    toast.style.zIndex = "99999";
    toast.style.boxShadow = "0 10px 30px rgba(0, 0, 0, 0.5)";
    toast.style.display = "flex";
    toast.style.alignItems = "center";
    toast.style.gap = "10px";
    toast.innerHTML = `<span>${type === 'success' ? '✓' : '⚠️'}</span> <span>${message}</span>`;

    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transition = "opacity 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
