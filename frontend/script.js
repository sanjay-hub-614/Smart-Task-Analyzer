async function analyzeTasks() {
    let rawInput = document.getElementById("taskInput").value.trim();
    let strategy = document.getElementById("strategy").value;

    if (rawInput === "") {
        alert("Please enter task JSON!");
        return;
    }

    let tasks;
    try {
        tasks = JSON.parse(rawInput);
    } catch (e) {
        alert("Invalid JSON format!");
        return;
    }

    const requestBody = {
        strategy: strategy,
        tasks: tasks
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody)
        });

        const result = await response.json();
        displayResults(result);

    } catch (error) {
        console.error("Error:", error);
        alert("Backend not reachable.");
    }
}

function displayResults(data) {
    const container = document.getElementById("results");
    container.innerHTML = ""; // clear previous

    data.forEach(task => {
        const card = document.createElement("div");
        card.classList.add("task-card");

        card.innerHTML = `
            <h3>${task.title}</h3>
            <p><strong>Due:</strong> ${task.due_date}</p>
            <p><strong>Importance:</strong> ${task.importance}</p>
            <p><strong>Hours:</strong> ${task.estimated_hours}</p>
            <p><strong>Score:</strong> ${task.score}</p>
        `;

        container.appendChild(card);
    });
}
