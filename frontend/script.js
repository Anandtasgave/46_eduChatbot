const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-btn");

function displayMessage(message, type) {
    const messageElement = document.createElement("p");
    messageElement.className = `${type}-message`;
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
}

sendButton.addEventListener("click", async () => {
    const message = userInput.value.trim();
    if (message === "") return;

    displayMessage(message, "user");

    userInput.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        if (response.ok) {
            const data = await response.json();
            displayMessage(data.response, "bot");
        } else {
            displayMessage("Sorry, something went wrong. Please try again.", "bot");
        }
    } catch (error) {
        displayMessage("Error connecting to the server. Please check your connection.", "bot");
    }
});

userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendButton.click();
    }
});