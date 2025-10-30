{/* 22.09.2025 */}

function appendMessage(sender, text, type = 'text') {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');

    if (sender === 'user') {
        messageDiv.classList.add('user-message');
        messageDiv.textContent = text;
    } else {
        messageDiv.classList.add('bot-message');
        if (type === 'thinking' || type === 'generating') {
            messageDiv.id = 'typing-indicator';
            messageDiv.innerHTML = text || 'Thinking...';
        } else {
            // Check if the response looks like a table and wrap it in a code block
            if (text.includes('|') && text.includes('-')) {
                const preElement = document.createElement('pre');
                preElement.textContent = text;
                const codeElement = document.createElement('code');
                codeElement.appendChild(preElement);
                messageDiv.appendChild(codeElement);
            } else {
                // Use marked.js to convert Markdown to HTML for normal text
                messageDiv.innerHTML = marked.parse(text);
            }
        }
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return messageDiv; // Return the created div for direct manipulation
}

function updateTypingIndicator(text) {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.textContent = text;
    }
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

async function handleChat(userInput) {
    appendMessage('user', userInput);
    const thinkingMessageDiv = appendMessage('bot', '', 'thinking');

    const systemPrompt = `You are a helpful and polite digital assistant. Your primary function is to engage in conversation and respond to user requests.
You have a specific, secondary ability: you can publish a text post on the user's LinkedIn profile using a tool called 'post_linkedin'.

**Tool Description:**
- **Tool Name:** post_linkedin
- **Function:** Publishes a text post to a LinkedIn profile.
- **Parameters:** { "content": string }

**Your Response Rules:**
1.  **Strictly Conversational Default:** Your default behavior is to be a conversational chatbot. You must respond with a standard text message for all general inquiries, including requests for content generation (e.g., "generate a wish for me," "write a poem," "draft an email").
2.  **Explicit Command for Tool Use:** You may ONLY use the 'post_linkedin' tool when the user's message contains a clear and unambiguous command to post the content to LinkedIn. The user's intent to post must be the primary goal of their message.
    - Examples of explicit commands: "Post this on LinkedIn: ...", "Please share this to my LinkedIn profile.", "Use the LinkedIn tool to post this content."
3.  **JSON Output for Tool Use:** When you detect an explicit command to use the tool, you must respond with a JSON object and nothing else.
    - The JSON object must have an "action" key with the value "post_linkedin" and an "arguments" key with an object containing the "content" of the post.
    - Do NOT include any additional text, explanations, or markdown in this response.

**Example Scenarios:**
- **User:** "Today is my birthday. Can you generate a wish for me?"
- **Your Correct Response (conversational):** "Happy birthday! Here's a wish for you: Wishing you a fantastic day filled with joy, laughter, and everything you've been hoping for. Happy birthday!"
- **User:** "Please post this on LinkedIn: 'Happy birthday to me! I'm celebrating another year of learning and growth.'"
- **Your Correct Response (JSON):** {"action": "post_linkedin", "arguments": {"content": "Happy birthday to me! I'm celebrating another year of learning and growth."}}`;
    const ollamaPayload = {
        model: 'phi3:mini',
        messages: [
            {
                role: 'system',
                content: systemPrompt
            },
            {
                role: 'user',
                content: userInput
            }
        ],
        options: {
            temperature: 0.0,
        },
        stream: true
    };

    let fullResponse = '';

    try {
        const response = await fetch('http://localhost:11434/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(ollamaPayload),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Ollama HTTP error! status: ${response.status}. Message: ${errorText}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let partialData = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            partialData += decoder.decode(value, { stream: true });

            const lines = partialData.split('\n');
            partialData = lines.pop();

            for (const line of lines) {
                if (line.trim() === '') continue;
                try {
                    const json = JSON.parse(line);
                    if (json.message && json.message.content) {
                        fullResponse += json.message.content;
                    }
                } catch (e) {
                    console.error('Error parsing stream chunk:', e);
                }
            }
            thinkingMessageDiv.textContent = fullResponse || 'Generating...';
        }

        removeTypingIndicator();

        // This is the key section that handles the JSON tool call from the LLM
        if (fullResponse.trim().startsWith('{') && fullResponse.trim().endsWith('}')) {
            try {
                const toolCall = JSON.parse(fullResponse);

                // This is the updated section that sends the API request
                appendMessage('bot', `_Initiating action: ${toolCall.action}..._`);

                const serverUrl = 'http://localhost:8000/execute_tool';
                const serverResponse = await fetch(serverUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: fullResponse, // Send the full JSON response received from Ollama
                });

                if (serverResponse.ok) {
                    const resultJson = await serverResponse.json();
                    appendMessage('bot', resultJson.result);
                } else {
                    const errorText = await serverResponse.text();
                    appendMessage('bot', `❌ Error from server: ${errorText}`);
                }

            } catch (err) {
                console.error("Failed to process tool JSON:", err);
                appendMessage('bot', '❌ Error: The model returned an invalid tool call or the server request failed.');
            }
        } else {
            const finalMessageDiv = appendMessage('bot', fullResponse);
            finalMessageDiv.innerHTML = marked.parse(fullResponse);
        }

    } catch (error) {
        console.error('Error calling Ollama:', error);
        removeTypingIndicator();
        appendMessage('bot', `❌ Error: ${error.message}`);
    }
}

const form = document.getElementById('message-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;
    document.getElementById('user-input').value = '';
    handleChat(userInput);
});


{/* 20.09.2025 */}

{ /*function appendMessage(sender, text, type = 'text') {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');

    if (sender === 'user') {
        messageDiv.classList.add('user-message');
        messageDiv.textContent = text;
    } else {
        messageDiv.classList.add('bot-message');
        if (type === 'thinking' || type === 'generating') {
            messageDiv.id = 'typing-indicator';
            messageDiv.innerHTML = text || 'Thinking...';
        } else {
            // Check if the response looks like a table and wrap it in a code block
            if (text.includes('|') && text.includes('-')) {
                const preElement = document.createElement('pre');
                preElement.textContent = text;
                const codeElement = document.createElement('code');
                codeElement.appendChild(preElement);
                messageDiv.appendChild(codeElement);
            } else {
                // Use marked.js to convert Markdown to HTML for normal text
                messageDiv.innerHTML = marked.parse(text);
            }
        }
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return messageDiv; // Return the created div for direct manipulation
}

function updateTypingIndicator(text) {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.textContent = text;
    }
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

async function handleChat(userInput) {
    appendMessage('user', userInput);
    const thinkingMessageDiv = appendMessage('bot', '', 'thinking');

    const systemPrompt = `You are a helpful and polite digital assistant. Your primary function is to engage in conversation and respond to user requests.
You have a specific, secondary ability: you can publish a text post on the user's LinkedIn profile using a tool called 'post_linkedin'.

**Tool Description:**
- **Tool Name:** post_linkedin
- **Function:** Publishes a text post on the user's LinkedIn profile.
- **Parameters:** { "content": string }

**Your Response Rules:**
1.  **Strictly Conversational Default:** Your default behavior is to be a conversational chatbot. You must respond with a standard text message for all general inquiries, including requests for content generation (e.g., "generate a wish for me," "write a poem," "draft an email").
2.  **Explicit Command for Tool Use:** You may ONLY use the 'post_linkedin' tool when the user's message contains a clear and unambiguous command to post the content to LinkedIn. The user's intent to post must be the primary goal of their message.
    - Examples of explicit commands: "Post this on LinkedIn: ...", "Please share this to my LinkedIn profile.", "Use the LinkedIn tool to post this content."
3.  **JSON Output for Tool Use:** When you detect an explicit command to use the tool, you must respond with a JSON object and nothing else.
    - The JSON object must have an "action" key with the value "post_linkedin" and an "arguments" key with an object containing the "content" of the post.
    - Do NOT include any additional text, explanations, or markdown in this response.

**Example Scenarios:**
- **User:** "Today is my birthday. Can you generate a wish for me?"
- **Your Correct Response (conversational):** "Happy birthday! Here's a wish for you: Wishing you a fantastic day filled with joy, laughter, and everything you've been hoping for. Happy birthday!"
- **User:** "Please post this on LinkedIn: 'Happy birthday to me! I'm celebrating another year of learning and growth.'"
- **Your Correct Response (JSON):** {"action": "post_linkedin", "arguments": {"content": "Happy birthday to me! I'm celebrating another year of learning and growth."}}`;
    const ollamaPayload = {
        model: 'phi3:mini',
        messages: [
            {
                role: 'system',
                content: systemPrompt
            },
            {
                role: 'user',
                content: userInput
            }
        ],
        options: {
            temperature: 0.0,
        },
        stream: true
    };

    let fullResponse = '';

    try {
        const response = await fetch('http://localhost:11434/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(ollamaPayload),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Ollama HTTP error! status: ${response.status}. Message: ${errorText}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let partialData = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            partialData += decoder.decode(value, { stream: true });

            const lines = partialData.split('\n');
            partialData = lines.pop();

            for (const line of lines) {
                if (line.trim() === '') continue;
                try {
                    const json = JSON.parse(line);
                    if (json.message && json.message.content) {
                        fullResponse += json.message.content;
                    }
                } catch (e) {
                    console.error('Error parsing stream chunk:', e);
                }
            }
            thinkingMessageDiv.textContent = fullResponse || 'Generating...';
        }

        removeTypingIndicator();

        // This is the key section that handles the JSON tool call from the LLM
        if (fullResponse.trim().startsWith('{') && fullResponse.trim().endsWith('}')) {
            try {
                const toolCall = JSON.parse(fullResponse);
                if (toolCall.action === "post_linkedin") {
                    appendMessage('bot', `_Initiating action: ${toolCall.action}..._`);

                    const serverUrl = 'http://localhost:5000/post_linkedin';
                    const serverResponse = await (await fetch(serverUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(toolCall.arguments),
                    })).text();

                    appendMessage('bot', serverResponse);
                }
            } catch (err) {
                console.error("Failed to parse tool JSON:", err);
                appendMessage('bot', '❌ Error: The model returned an invalid tool call format.');
            }
        } else {
            const finalMessageDiv = appendMessage('bot', fullResponse);
            finalMessageDiv.innerHTML = marked.parse(fullResponse);
        }

    } catch (error) {
        console.error('Error calling Ollama:', error);
        removeTypingIndicator();
        appendMessage('bot', `❌ Error: ${error.message}`);
    }
}

const form = document.getElementById('message-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;
    document.getElementById('user-input').value = '';
    handleChat(userInput);
});
*/} 
