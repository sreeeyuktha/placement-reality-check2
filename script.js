document.getElementById("checkBtn").addEventListener("click", checkPlacement);

async function checkPlacement() {

    const skills = document.getElementById("skillsInput").value;
    const dreamJob = document.getElementById("dreamJob").value;
    const resultDiv = document.getElementById("result");

    if (skills.trim() === "" || dreamJob === "") {
        alert("Please enter skills and select a dream job.");
        return;
    }

    resultDiv.innerHTML = "⏳ Checking your placement readiness...";

    try {
        const response = await fetch("http://localhost:5000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                skills: skills,
                dream_job: dreamJob
            })
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        // If backend sends error
        if (data.error) {
            resultDiv.innerHTML = `❌ ${data.error}`;
            return;
        }

        resultDiv.innerHTML = `
            <h3>📊 Placement Report</h3>
            <p><strong>Dream Job:</strong> ${data.dream_job}</p>
            <p><strong>Expected Salary:</strong> ${data.salary}</p>

            <p><strong>Matched Skills:</strong> ${data.matched_skills.length > 0 ? data.matched_skills.join(", ") : "None"}</p>
            <p><strong>Missing Skills:</strong> ${data.missing_skills.join(", ")}</p>

            <p><strong>Resume Score:</strong> ${data.score.toFixed(2)}%</p>

            <p><strong>Status:</strong> ${data.message}</p>
        `;

    } catch (error) {
        resultDiv.innerHTML = `
            ❌ Cannot connect to server.<br>
            Make sure:
            <ul>
                <li>Python server is running</li>
                <li>Server is running on port 5000</li>
                <li>You opened index.html after starting server</li>
            </ul>
        `;
    }
}
