async function getChatbotResponse(message) {
    try {
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json", 
            },
            body: JSON.stringify({ message: message }) 
        });

        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }

        const data = await response.json();

        return data.response;
    } catch (error) {
        console.error('Error:', error);
        return "Sorry, there was an error. Please try again later.";
    }
}

document.getElementById("sendBtn").addEventListener("click", async function() {
    const userInput = document.getElementById("userInput").value;

    if (userInput.trim() === "") {
        alert("Please enter a message.");
        return;
    }

    document.getElementById("userInput").value = "";

    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += `<div class="user-message">${userInput}</div>`;

    const response = await getChatbotResponse(userInput);

    chatBox.innerHTML += `<div class="bot-response">${response}</div>`;

    chatBox.scrollTop = chatBox.scrollHeight;
});