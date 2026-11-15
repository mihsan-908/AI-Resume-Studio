document.addEventListener("DOMContentLoaded", function () {
    const data = window.ANALYSIS_DATA || {};

    // 1. ATS Score Doughnut Gauge
    const atsCtx = document.getElementById("atsGaugeChart");
    if (atsCtx) {
        const atsScore = data.ats_score || 0;
        const color = atsScore >= 75 ? "#22c55e" : (atsScore >= 50 ? "#eab308" : "#ef4444");

        new Chart(atsCtx, {
            type: "doughnut",
            data: {
                datasets: [{
                    data: [atsScore, 100 - atsScore],
                    backgroundColor: [color, "#1e293b"],
                    borderWidth: 0,
                    circumference: 260,
                    rotation: 230
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "80%",
                plugins: { legend: { display: false }, tooltip: { enabled: false } }
            }
        });
    }

    // 2. Job Match Gauge
    const matchCtx = document.getElementById("matchGaugeChart");
    if (matchCtx && data.match_score !== null && data.match_score !== undefined) {
        const matchScore = data.match_score;
        new Chart(matchCtx, {
            type: "doughnut",
            data: {
                datasets: [{
                    data: [matchScore, 100 - matchScore],
                    backgroundColor: ["#a855f7", "#1e293b"],
                    borderWidth: 0,
                    circumference: 260,
                    rotation: 230
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "80%",
                plugins: { legend: { display: false }, tooltip: { enabled: false } }
            }
        });
    }

    // 3. Skill Category Doughnut Chart
    const skillsCtx = document.getElementById("skillsCategoryChart");
    if (skillsCtx) {
        new Chart(skillsCtx, {
            type: "doughnut",
            data: {
                labels: ["Programming", "AI/ML", "Frameworks", "Databases", "Tools"],
                datasets: [{
                    data: [4, 3, 3, 2, 4],
                    backgroundColor: ["#38bdf8", "#a855f7", "#22c55e", "#eab308", "#64748b"],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: "right", labels: { color: "#94a3b8" } } }
            }
        });
    }

    // 4. Resume Section Completeness Bar Chart
    const compCtx = document.getElementById("completenessBarChart");
    if (compCtx) {
        new Chart(compCtx, {
            type: "bar",
            data: {
                labels: ["Summary", "Skills", "Projects", "Experience", "Certifications"],
                datasets: [{
                    label: "Completeness %",
                    data: [90, 85, 95, 20, 10],
                    backgroundColor: "#0284c7",
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { min: 0, max: 100, grid: { color: "#334155" }, ticks: { color: "#94a3b8" } },
                    x: { grid: { display: false }, ticks: { color: "#94a3b8" } }
                }
            }
        });
    }
});
