const chatContainer = document.getElementById('chat-container');
const chatInput = document.getElementById('chat-input');

function appendMessage(message, isUser) {
    const messageElement = document.createElement('div');
    messageElement.innerText = message;
    messageElement.classList.add('message');

    if (isUser) {
        messageElement.classList.add('user-message');
    } else {
        messageElement.classList.add('bot-message');
    }

    chatContainer.appendChild(messageElement);

    // Scroll to the bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

chatInput.addEventListener('keypress', async function (e) {
    if (e.key === 'Enter') {
        const userQuery = chatInput.value.trim();

        if (userQuery !== '') {
            appendMessage(`You: ${userQuery}`, true);
            chatInput.value = '';

            // Send the user query to the server
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: userQuery }),
            });

            const result = await response.json();
            appendMessage(`Bot: ${result.result}`, false);
        }
    }
});
