// Tap Bonds AI Assistant - Main JavaScript

// Initialize marked.js with options
marked.setOptions({
    breaks: true,
    gfm: true,
    headerIds: false,
    mangle: false
});

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const newChatBtn = document.getElementById('newChatBtn');
    const exampleQueries = document.getElementById('exampleQueries');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');

    // Focus on input field when page loads
    userInput.focus();

    // Function to add a message to the chat
    function addMessage(content, isUser, agentInfo = '') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'} fade-in`;
        
        if (isUser) {
            messageDiv.textContent = content;
        } else {
            const contentDiv = document.createElement('div');
            contentDiv.className = 'markdown-content';
            contentDiv.innerHTML = marked.parse(content);
            messageDiv.appendChild(contentDiv);
            
            if (agentInfo) {
                const agentDiv = document.createElement('div');
                agentDiv.className = 'agent-info';
                agentDiv.textContent = `Agent: ${agentInfo}`;
                messageDiv.appendChild(agentDiv);
            }
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Hide example queries after first message
        if (chatMessages.children.length > 1) {
            exampleQueries.style.display = 'none';
        }
    }

    // Function to send a message to the API
    async function sendMessage(message) {
        try {
            loadingIndicator.style.display = 'block';
            
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: message })
            });
            
            const data = await response.json();
            
            loadingIndicator.style.display = 'none';
            
            if (data.error) {
                addMessage(`Error: ${data.error}`, false);
            } else {
                addMessage(data.response, false, data.agent);
            }
        } catch (error) {
            loadingIndicator.style.display = 'none';
            addMessage(`Error: ${error.message}`, false);
        }
    }

    // Function to start a new chat
    function startNewChat() {
        // Clear chat messages except the first welcome message
        while (chatMessages.children.length > 1) {
            chatMessages.removeChild(chatMessages.lastChild);
        }
        
        // Show example queries again
        exampleQueries.style.display = 'block';
        
        // Clear input field
        userInput.value = '';
        
        // Focus on input field
        userInput.focus();

        // Add a subtle animation to the welcome message
        chatMessages.firstElementChild.classList.add('fade-in');
        setTimeout(() => {
            chatMessages.firstElementChild.classList.remove('fade-in');
        }, 500);
    }

    // Function to copy conversation to clipboard
    function copyConversation() {
        let conversationText = '';
        
        // Loop through all messages and extract their text content
        Array.from(chatMessages.children).forEach(message => {
            if (message.classList.contains('user-message')) {
                conversationText += `User: ${message.textContent}\n\n`;
            } else {
                const content = message.querySelector('.markdown-content');
                if (content) {
                    // Remove HTML tags for plain text
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = content.innerHTML;
                    conversationText += `Assistant: ${tempDiv.textContent.trim()}\n\n`;
                }
            }
        });
        
        // Copy to clipboard
        navigator.clipboard.writeText(conversationText)
            .then(() => {
                // Show a temporary tooltip or notification
                const tooltip = document.createElement('div');
                tooltip.className = 'copy-tooltip fade-in';
                tooltip.textContent = 'Conversation copied!';
                document.body.appendChild(tooltip);
                
                // Position the tooltip near the copy button
                const rect = copyBtn.getBoundingClientRect();
                tooltip.style.position = 'absolute';
                tooltip.style.top = `${rect.top - 40}px`;
                tooltip.style.left = `${rect.left}px`;
                
                // Remove the tooltip after a delay
                setTimeout(() => {
                    tooltip.classList.add('fade-out');
                    setTimeout(() => {
                        document.body.removeChild(tooltip);
                    }, 300);
                }, 2000);
            })
            .catch(err => {
                console.error('Failed to copy conversation: ', err);
            });
    }

    // Event listener for send button
    sendButton.addEventListener('click', function() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            sendMessage(message);
        }
    });

    // Event listener for Enter key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const message = userInput.value.trim();
            if (message) {
                addMessage(message, true);
                userInput.value = '';
                sendMessage(message);
            }
        }
    });

    // Event listener for new chat button
    newChatBtn.addEventListener('click', startNewChat);

    // Event listener for clear button
    clearBtn.addEventListener('click', startNewChat);

    // Event listener for copy button
    copyBtn.addEventListener('click', copyConversation);

    // Event listeners for example queries
    document.querySelectorAll('.example-query').forEach(function(element) {
        element.addEventListener('click', function() {
            // Extract the text without the icon
            const iconElement = this.querySelector('i');
            let query = this.textContent;
            
            if (iconElement) {
                // Remove the icon's text content from the query
                query = query.replace(iconElement.textContent, '').trim();
            }
            
            userInput.value = query;
            addMessage(query, true);
            sendMessage(query);
        });
    });

    // Function to get available agents
    async function getAgents() {
        try {
            const response = await fetch('/api/agents');
            const data = await response.json();
            
            console.log('Available agents:', data.agents);
        } catch (error) {
            console.error('Error fetching agents:', error);
        }
    }

    // Get available agents when page loads
    getAgents();

    // Add event listener for window resize to adjust chat container height
    window.addEventListener('resize', function() {
        adjustChatHeight();
    });

    // Function to adjust chat height based on window size
    function adjustChatHeight() {
        const windowHeight = window.innerHeight;
        const chatContainer = document.querySelector('.chat-container');
        const chatHeader = document.querySelector('.chat-header');
        const chatInput = document.querySelector('.chat-input');
        const loadingDiv = document.querySelector('.loading');
        const exampleQueriesDiv = document.querySelector('.example-queries');
        const footer = document.querySelector('footer');
        
        if (windowHeight < 600) {
            chatMessages.style.height = '200px';
        } else if (windowHeight < 800) {
            chatMessages.style.height = '300px';
        } else {
            chatMessages.style.height = '400px';
        }
    }

    // Initial adjustment
    adjustChatHeight();

    // Add CSS for the copy tooltip
    const style = document.createElement('style');
    style.textContent = `
        .copy-tooltip {
            background-color: #333;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .fade-out {
            opacity: 0;
            transition: opacity 0.3s;
        }
    `;
    document.head.appendChild(style);
}); 