document.addEventListener("DOMContentLoaded", function () {
    // 1. ATS Score Trend & Distribution Line Chart
    const trendCtx = document.getElementById("scoreTrendChart");
    if (trendCtx) {
        const ctx = trendCtx.getContext("2d");
        const gradient = ctx.createLinearGradient(0, 0, 0, 240);
        gradient.addColorStop(0, "rgba(56, 189, 248, 0.28)");
        gradient.addColorStop(1, "rgba(56, 189, 248, 0.0)");

        new Chart(trendCtx, {
            type: "line",
            data: {
                labels: ["Run #1", "Run #2", "Run #3", "Run #4", "Run #5"],
                datasets: [{
                    label: "ATS Score",
                    data: [64, 68, 74, 82, 88],
                    borderColor: "#38bdf8",
                    borderWidth: 2.5,
                    backgroundColor: gradient,
                    fill: true,
                    tension: 0.35,
                    pointBackgroundColor: "#38bdf8",
                    pointBorderColor: "#0f172a",
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: "#ffffff",
                    pointHoverBorderColor: "#38bdf8"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: "#1e293b",
                        titleColor: "#f8fafc",
                        bodyColor: "#38bdf8",
                        borderColor: "#334155",
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false,
                        callbacks: {
                            label: function (context) {
                                return `ATS Score: ${context.parsed.y} / 100`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        grid: {
                            color: "rgba(51, 65, 85, 0.5)",
                            drawBorder: false
                        },
                        ticks: {
                            color: "#94a3b8",
                            stepSize: 20,
                            font: { family: "Inter", size: 11 }
                        }
                    },
                    x: {
                        grid: {
                            color: "rgba(51, 65, 85, 0.2)",
                            drawBorder: false
                        },
                        ticks: {
                            color: "#94a3b8",
                            font: { family: "Inter", size: 11 }
                        }
                    }
                }
            }
        });
    }

    // 2. Resume Quality Breakdown Doughnut Chart
    const qualityCtx = document.getElementById("qualityPieChart");
    if (qualityCtx) {
        new Chart(qualityCtx, {
            type: "doughnut",
            data: {
                labels: ["Excellent (80+)", "Good (60-79)", "Needs Work (<60)"],
                datasets: [{
                    data: [45, 35, 20],
                    backgroundColor: [
                        "#22c55e",
                        "#eab308",
                        "#ef4444"
                    ],
                    borderWidth: 3,
                    borderColor: "#1e293b",
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "70%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            color: "#94a3b8",
                            boxWidth: 12,
                            boxHeight: 12,
                            padding: 16,
                            font: { family: "Inter", size: 11, weight: 500 }
                        }
                    },
                    tooltip: {
                        backgroundColor: "#1e293b",
                        titleColor: "#f8fafc",
                        bodyColor: "#e2e8f0",
                        borderColor: "#334155",
                        borderWidth: 1,
                        padding: 10,
                        callbacks: {
                            label: function (context) {
                                return ` ${context.label}: ${context.parsed}%`;
                            }
                        }
                    }
                }
            }
        });
    }
});
