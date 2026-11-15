let targetDeleteId = null;

function filterHistoryTable() {
    const input = document.getElementById("historySearch").value.toLowerCase();
    const rows = document.querySelectorAll("#historyTable tbody tr:not(#emptyHistoryRow)");
    let visibleCount = 0;

    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        if (text.includes(input)) {
            row.style.display = "";
            visibleCount++;
        } else {
            row.style.display = "none";
        }
    });

    const countElem = document.getElementById("recordCount");
    if (countElem) {
        countElem.innerText = visibleCount;
    }
}

function confirmDelete(id) {
    targetDeleteId = id;
    const targetLabel = document.getElementById("deleteTargetId");
    if (targetLabel) targetLabel.innerText = `#${id}`;
    const modal = document.getElementById("deleteModal");
    if (modal) modal.style.display = "flex";
}

function closeDeleteModal() {
    targetDeleteId = null;
    const modal = document.getElementById("deleteModal");
    if (modal) modal.style.display = "none";
}

async function executeDelete() {
    if (!targetDeleteId) return;

    try {
        const response = await fetch(`/api/analyses/${targetDeleteId}`, {
            method: "DELETE"
        });

        const resData = await response.json();
        if (!response.ok) throw new Error(resData.detail || "Deletion failed.");

        const row = document.getElementById(`row-${targetDeleteId}`);
        if (row) {
            row.remove();
            const countElem = document.getElementById("recordCount");
            if (countElem) {
                const current = parseInt(countElem.innerText, 10) || 1;
                countElem.innerText = Math.max(0, current - 1);
            }
        }

        const alertBox = document.getElementById("historyAlert");
        if (alertBox) {
            alertBox.className = "alert alert-success";
            alertBox.innerText = `✓ Analysis #${targetDeleteId} was permanently deleted from PostgreSQL.`;
            alertBox.style.display = "block";
            setTimeout(() => { alertBox.style.display = "none"; }, 4000);
        }

    } catch (err) {
        alert(err.message || "Failed to delete record.");
    } finally {
        closeDeleteModal();
    }
}
