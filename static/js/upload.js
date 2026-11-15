function handleFileSelected(event) {
    const file = event.target.files[0];
    const badge = document.getElementById("fileSelectedBadge");
    const prompt = document.getElementById("dropzonePrompt");

    if (file) {
        if (file.size > 10 * 1024 * 1024) {
            alert("File size exceeds 10MB limit.");
            event.target.value = "";
            badge.style.display = "none";
            return;
        }
        badge.style.display = "block";
        badge.innerHTML = `✓ Selected: <strong>${file.name}</strong> (${(file.size / 1024).toFixed(1)} KB)`;
    } else {
        badge.style.display = "none";
    }
}

// Drag & drop highlight
const dropzone = document.getElementById("dropzone");
if (dropzone) {
    ["dragenter", "dragover"].forEach(name => {
        dropzone.addEventListener(name, (e) => {
            e.preventDefault();
            dropzone.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach(name => {
        dropzone.addEventListener(name, (e) => {
            e.preventDefault();
            dropzone.classList.remove("dragover");
        });
    });

    dropzone.addEventListener("drop", (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const fileInput = document.getElementById("resumeFileInput");
            fileInput.files = files;
            handleFileSelected({ target: fileInput });
        }
    });
}

async function submitAnalysis(event) {
    event.preventDefault();

    const fileInput = document.getElementById("resumeFileInput");
    const jobDescInput = document.getElementById("jobDescInput");
    const errorBanner = document.getElementById("uploadError");
    const modal = document.getElementById("processingModal");
    const btn = document.getElementById("analyzeBtn");
    const btnSpinner = document.getElementById("btnSpinner");
    const progressFill = document.getElementById("progressBarFill");
    const statusTitle = document.getElementById("stepStatusTitle");

    errorBanner.style.display = "none";

    if (!fileInput.files[0]) {
        errorBanner.innerText = "Please select a PDF or TXT resume file.";
        errorBanner.style.display = "block";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    if (jobDescInput.value.trim()) {
        formData.append("job_description", jobDescInput.value.trim());
    }

    modal.style.display = "flex";
    btn.disabled = true;

    // Simulated progress steps
    let progress = 20;
    const interval = setInterval(() => {
        progress += 15;
        if (progress > 85) progress = 85;
        progressFill.style.width = progress + "%";

        if (progress === 35) statusTitle.innerText = "Extracting Structured Resume Data...";
        else if (progress === 50) statusTitle.innerText = "Evaluating ATS Compatibility...";
        else if (progress === 65) statusTitle.innerText = "Matching Job Skills & Requirements...";
        else if (progress === 80) statusTitle.innerText = "Generating Professional AI Rewrite...";
    }, 2500);

    try {
        const response = await fetch("/api/resumes/analyze", {
            method: "POST",
            body: formData
        });

        clearInterval(interval);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Analysis failed.");
        }

        progressFill.style.width = "100%";
        statusTitle.innerText = "Analysis Complete! Redirecting...";

        setTimeout(() => {
            window.location.href = `/results/${result.analysis_id}`;
        }, 500);

    } catch (err) {
        clearInterval(interval);
        modal.style.display = "none";
        btn.disabled = false;
        errorBanner.innerText = err.message || "An unexpected error occurred during processing.";
        errorBanner.style.display = "block";
    }
}
