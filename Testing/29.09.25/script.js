// A global variable to store the fetched tools, so we only fetch them once
let availableTools = [];
const numThreads = 8;

// --- All other functions (appendMessage, etc.) remain the same ---
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
            if (text.includes('|') && text.includes('-')) {
                const preElement = document.createElement('pre');
                preElement.textContent = text;
                const codeElement = document.createElement('code');
                codeElement.appendChild(preElement);
                messageDiv.appendChild(codeElement);
            } else {
                messageDiv.innerHTML = marked.parse(text);
            }
        }
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return messageDiv;
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

// Fetches tools from the MCP server only ONCE
async function fetchTools() {
    try {
        const response = await fetch('http://localhost:8000/tools');
        if (!response.ok) {
            throw new Error(`Failed to fetch tools: ${response.status} ${response.statusText}`);
        }
        availableTools = await response.json();
        console.log("Tools fetched successfully:", availableTools);
    } catch (error) {
        console.error('Error fetching tools:', error);
        appendMessage('bot', `❌ Error fetching tools: ${error.message}`);
    }
}

// ⭐ Corrected: This is the classifier function that uses the phi3:mini model.
// It returns a promise that resolves to the determined intent.
async function classifyIntent(userInput) {
    const classifierPrompt = `You are a text classifier. Your task is to analyze a user's message and determine their intent.
    
### Instructions
1. **TOOL_CALL:** If the user's message is a command to perform an action on LinkedIn, or if the user's message is a statement that implies a need for a tool, your response MUST be the single word: 'TOOL_CALL'.
2. **CONVERSATION:** If the user's message is a general greeting or a question about a topic (like "what is a language model?"), your response MUST be the single word: 'CONVERSATION'.
    
### Examples (for better accuracy)
* **TOOL_CALL**
    - "Post this content on LinkedIn: Today is a great day!"
    - "I'd like to share this on LinkedIn."
    - "Can you help me post this on LinkedIn?"
    - "Post this content on LinkedIn, 'Hello everyone! Today is a new day.'"
    - "Hello. Can you post this on my profile: I'm enjoying my trip."
* **CONVERSATION**
    - "Hello."
    - "How are you?"
    - "What is your purpose?"
    - "Tell me about yourself."
    - "That's a nice thought."
    
You must ONLY respond with 'TOOL_CALL' or 'CONVERSATION'. No other words, no punctuation, no explanations.`;

    const payload = {
        model: 'phi3:mini', // Using the fast, small model for classification
        messages: [{
            role: 'system',
            content: classifierPrompt,
        }, {
            role: 'user',
            content: userInput,
        }],
        options: {
            temperature: 0.0,
            num_thread: numThreads
        },
        stream: false, // We need the full response at once
    };

    try {
        const response = await fetch('http://localhost:11434/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Ollama HTTP error during classification: ${response.status}. Message: ${errorText}`);
        }
        
        const jsonResponse = await response.json();
        return jsonResponse.message.content.trim(); // Return the single word
    } catch (error) {
        console.error('Error during classification:', error);
        // Fallback to conversation if classification fails
        return 'CONVERSATION';
    }
}

// ⭐ Corrected: This function now handles streaming more robustly.
async function handleChat(userInput) {
    appendMessage('user', userInput);
    const thinkingMessageDiv = appendMessage('bot', '', 'thinking');

    const intent = await classifyIntent(userInput);
    console.log(`User intent classified as: ${intent}`);

    let ollamaPayload;
    
    if (intent === 'TOOL_CALL') {
        updateTypingIndicator('Detected a tool-calling request...');
        ollamaPayload = {
            model: 'llama3.1:8b-instruct-q4_K_M',
            messages: [{
                role: 'system',
                content: `You are a helpful and polite digital assistant. Your primary function is to respond to user requests by using the available tools.
                You have access to a set of tools to perform specific actions on behalf of the user.
                
                ### Instructions
                1. **Identify Clear Intent:** Only use a tool when the user's message contains a clear and unambiguous command to perform a specific action that one of your tools can execute.
                2. **Be Precise:** Do not guess or assume the user's intent. If the request is vague, ask for clarification.
                3. **Follow the Schema:** When using a tool, you must follow the provided JSON schema exactly.
                
                ### Examples of User Actions (USE A TOOL):
                - "Post this to my LinkedIn: Today is a great day!"
                - "Can you share 'My first blog post is live!' on LinkedIn?"
                
                Remember, your default behavior to be a helpful assistant. Only act as an agent when the user explicitly instructs you to.`,
            }, {
                role: 'user',
                content: userInput,
            }],
            tools: availableTools,
            stream: true,
            options: {
                num_thread: numThreads,
            }
        };
    } else {
        updateTypingIndicator('Responding conversationally...');
        ollamaPayload = {
            model: 'phi3:mini',
            messages: [{
                role: 'system',
                content: `You are a helpful and polite digital assistant. Your primary function is to engage in conversation and respond to user requests. You do not have access to any external tools.`,
            }, {
                role: 'user',
                content: userInput,
            }],
            stream: true,
            options: {
                num_thread: numThreads,
            },
        };
    }

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
        let fullResponse = '';
        let isToolCallHandled = false;

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
                    
                    if (json.message && json.message.tool_calls && !isToolCallHandled) {
                        const toolCall = json.message.tool_calls[0];
                        removeTypingIndicator();
                        appendMessage('bot', `_Initiating action: ${toolCall.function.name}..._`);

                        const serverUrl = 'http://localhost:8000/execute_tool';
                        const serverResponse = await fetch(serverUrl, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                action: toolCall.function.name,
                                arguments: toolCall.function.arguments
                            }),
                        });

                        if (serverResponse.ok) {
                            const resultJson = await serverResponse.json();
                            appendMessage('bot', resultJson.result);
                        } else {
                            const errorText = await serverResponse.text();
                            appendMessage('bot', `❌ Error from server: ${errorText}`);
                        }
                        isToolCallHandled = true;
                        // Break out of the for loop
                        break;
                    }
                    if (json.message && json.message.content) {
                        fullResponse += json.message.content;
                    }
                } catch (e) {
                    console.error('Error parsing stream chunk:', e);
                }
            }
            if (isToolCallHandled) {
                // Break out of the while loop to stop the stream
                break;
            }
            thinkingMessageDiv.textContent = fullResponse || 'Generating...';
        }
        
        // Final message processing after the stream is done
        if (!isToolCallHandled && fullResponse) {
            removeTypingIndicator();
            const finalMessageDiv = appendMessage('bot', fullResponse);
            finalMessageDiv.innerHTML = marked.parse(fullResponse);
        } else if (!isToolCallHandled) {
             removeTypingIndicator();
             appendMessage('bot', "I'm sorry, I couldn't generate a response. Please try again.");
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

// Fetch tools as soon as the page loads
document.addEventListener('DOMContentLoaded', fetchTools);