function openSettings() {
  document.getElementById("settingsScreen").classList.remove("hidden");
}

function closeSettings() {
  document.getElementById("settingsScreen").classList.add("hidden");
}

async function loadTemplates() {
  const response = await fetch("/api/templates");
  const templates = await response.json();

  const deviceList = document.getElementById("deviceList");
  deviceList.innerHTML = "";

  templates.forEach(template => {
    const card = document.createElement("div");
    card.className = "device-card";

    card.innerHTML = `
      <div>
        <h3>${template.device_name}</h3>
        <p>Template: ${template.template_name}</p>
        <p>Command: ${template.command}</p>

        <button onclick="runCommand('${template.command}')">Run</button>
        <button class="delete-btn" onclick="deleteTemplate(${template.id})">Delete</button>
      </div>
    `;

    deviceList.appendChild(card);
  });
}

async function saveSettings() {
  const deviceName = document.getElementById("deviceName").value;
  const templateName = document.getElementById("templateName").value;
  const command = document.getElementById("commandSelect").value;

  const data = {
    deviceName: deviceName,
    templateName: templateName,
    command: command
  };

  await fetch("/api/templates", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  document.getElementById("statusText").innerText = "Saved to SQLite database!";

  document.getElementById("deviceName").value = "";
  document.getElementById("templateName").value = "";

  closeSettings();
  loadTemplates();
}

async function deleteTemplate(id) {
  await fetch(`/api/templates/${id}`, {
    method: "DELETE"
  });

  document.getElementById("statusText").innerText = "Template deleted.";
  loadTemplates();
}

function runCommand(command) {
  if (command === "Turn_Light_On") {
    document.getElementById("statusText").innerText = "Turning light on...";
  } 
  else if (command === "Turn_Light_Off") {
    document.getElementById("statusText").innerText = "Turning light off...";
  } 
  else if (command === "Play_Music") {
    document.getElementById("statusText").innerText = "Playing music...";
  } 
  else if (command === "Stop_Music") {
    document.getElementById("statusText").innerText = "Stopping music...";
  } 
  else if (command === "Turn_Volume_Up") {
    document.getElementById("statusText").innerText = "Turning volume up...";
  } 
  else if (command === "Turn_Volume_Down") {
    document.getElementById("statusText").innerText = "Turning volume down...";
  } 
  else {
    document.getElementById("statusText").innerText = "Unknown command.";
  }
}

window.onload = loadTemplates;