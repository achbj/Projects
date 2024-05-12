const chatHistory = document.getElementById("chatHistory");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");

sendButton.addEventListener("click", submitQuery);

function submitQuery() {
  const query = userInput.value.trim();
  if (query !== "") {
    appendMessage("User", query);
    // Send the user's query to Flask endpoint
    fetch("/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "user_input=" + encodeURIComponent(query),
    })
      .then((response) => response.json())
      .then((data) => {
        appendMessage("AI", data.response);
        userInput.value = "";
      })
      .catch((error) => console.error("Error:", error));
  }
}

function appendMessage(sender, message) {
  const messageElement = document.createElement("div");
  messageElement.className = "message";
  messageElement.innerHTML = `
        <span class="${sender.toLowerCase()}-label">${sender}:</span>
        <span>${message}</span>
    `;
  chatHistory.appendChild(messageElement);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

userInput.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    submitQuery();
  }
});
