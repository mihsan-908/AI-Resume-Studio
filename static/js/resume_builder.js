async function saveResumeEdits() {
    const analysisId = window.ANALYSIS_ID;
    if (!analysisId) return;

    const saveBtn = document.getElementById("saveBtn");
    const alertBox = document.getElementById("builderAlert");

    // Gather edited fields
    const summary = document.getElementById("editSummary").value.trim();

    const skills = {
        "Programming Languages": parseCommaList(document.getElementById("skill_Programming_Languages").value),
        "AI & Machine Learning": parseCommaList(document.getElementById("skill_AI_ML").value),
        "Frameworks": parseCommaList(document.getElementById("skill_Frameworks").value),
        "Databases": parseCommaList(document.getElementById("skill_Databases").value),
        "Tools & Platforms": parseCommaList(document.getElementById("skill_Tools").value)
    };

    // Gather projects
    const projectCards = document.querySelectorAll(".project-edit-card");
    const projects = [];
    projectCards.forEach(card => {
        const title = card.querySelector(".proj-title-input").value.trim();
        const bulletsText = card.querySelector(".proj-bullets-input").value;
        const bullets = bulletsText.split("\n").map(b => b.trim()).filter(b => b.length > 0);
        if (title) {
            projects.push({
                title: title,
                rewritten_description: bullets
            });
        }
    });

    const tipsText = document.getElementById("editTips").value;
    const tips = tipsText.split("\n").map(t => t.trim()).filter(t => t.length > 0);

    const payload = {
        professional_summary: summary,
        skills: skills,
        projects: projects,
        final_resume_tips: tips
    };

    saveBtn.disabled = true;
    saveBtn.innerText = "Saving...";

    try {
        const response = await fetch(`/api/analyses/${analysisId}/resume`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const resData = await response.json();
        if (!response.ok) throw new Error(resData.detail || "Failed to save edits.");

        alertBox.className = "alert alert-success";
        alertBox.innerText = `✓ Changes saved successfully (Version ${resData.version})! Exports will now generate from your approved content.`;
        alertBox.style.display = "block";
        setTimeout(() => alertBox.style.display = "none", 5000);

    } catch (err) {
        alertBox.className = "alert alert-danger";
        alertBox.innerText = err.message || "Error saving edits.";
        alertBox.style.display = "block";
    } finally {
        saveBtn.disabled = false;
        saveBtn.innerText = "💾 Save Changes";
    }
}

function parseCommaList(str) {
    if (!str) return [];
    return str.split(",").map(s => s.trim()).filter(s => s.length > 0);
}
