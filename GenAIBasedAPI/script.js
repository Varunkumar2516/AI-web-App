document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('.nav-link');
    const toolContents = document.querySelectorAll('.tool-content');
    const welcomeScreen = document.getElementById('welcome-screen');
    const API_URL = 'http://127.0.0.1:5000';

    // --- NAVIGATION ---
    function switchTool(toolId) {
        welcomeScreen.classList.remove('active');
        toolContents.forEach(content => content.classList.remove('active'));
        navLinks.forEach(link => link.classList.remove('active'));
        document.getElementById(`${toolId}-tool`)?.classList.add('active');
        document.querySelector(`[data-tool="${toolId}"]`)?.classList.add('active');
    }
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            switchTool(link.getAttribute('data-tool'));
        });
    });

    // --- GENERIC API HANDLER FOR TEXT-BASED TOOLS ---
    async function handleTextApiRequest(toolId, endpoint, payloadKey, data) {
        const responseArea = document.querySelector(`#${toolId}-tool .response-area`);
        responseArea.innerHTML = 'Generating...'; // Use innerHTML
        try {
            const response = await fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ [payloadKey]: data }),
            });
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const result = await response.json();
            
            // ** THE FIX IS HERE: Convert Markdown to HTML **
            responseArea.innerHTML = marked.parse(result.response);

        } catch (error) {
            console.error("API Error:", error);
            responseArea.innerHTML = `Error: Could not get a response. Please ensure the backend server is running.`;
        }
    }

    // --- TOOL: CHATBOT ---
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSendBtn = document.getElementById('chatbot-send-btn');
    const chatDisplay = document.querySelector('.chat-display');
    function addChatMessage(message, sender, isMarkdown = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        // ** THE FIX IS HERE: Render AI messages as HTML **
        if (isMarkdown) {
            messageDiv.innerHTML = marked.parse(message);
        } else {
            messageDiv.textContent = message;
        }

        chatDisplay.appendChild(messageDiv);
        chatDisplay.scrollTop = chatDisplay.scrollHeight;
    }
    async function handleChatbotSubmit() {
        const userInput = chatbotInput.value.trim();
        if (userInput) {
            addChatMessage(userInput, 'user', false); // User input is plain text
            chatbotInput.value = '';
            
            // Add a temporary "typing" message for immediate feedback
            const thinkingMsg = document.createElement('div');
            thinkingMsg.className = 'message ai-message';
            thinkingMsg.innerHTML = '...';
            chatDisplay.appendChild(thinkingMsg);
            chatDisplay.scrollTop = chatDisplay.scrollHeight;

            try {
                const response = await fetch(`${API_URL}/api/chatbot`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: userInput }),
                });
                if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
                const data = await response.json();
                
                // ** THE FIX IS HERE: Update the "thinking" message with formatted HTML **
                thinkingMsg.innerHTML = marked.parse(data.response);

            } catch (error) {
                thinkingMsg.innerHTML = 'Sorry, something went wrong. Please try again.';
            }
        }
    }
    chatbotSendBtn.addEventListener('click', handleChatbotSubmit);
    chatbotInput.addEventListener('keypress', e => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleChatbotSubmit()));

    // --- Connect ALL other tools ---
    function setupTool(toolId, endpoint, payloadKey, inputType = 'textarea') {
        const toolDiv = document.querySelector(`#${toolId}-tool`);
        const button = toolDiv.querySelector('button');
        const input = toolDiv.querySelector(inputType);
        button.addEventListener('click', () => {
            if (input.value.trim()) {
                handleTextApiRequest(toolId, endpoint, payloadKey, input.value);
            }
        });
    }

    setupTool('summarizer', '/api/summarize', 'text');
    setupTool('writer', '/api/creative-writer', 'prompt');
    setupTool('notes', '/api/make-notes', 'text');
    setupTool('ideas', '/api/generate-ideas', 'prompt');
    setupTool('translator', '/api/translate', 'text');
    setupTool('code-explainer', '/api/explain-code', 'code');
    setupTool('sentiment', '/api/sentiment-analyzer', 'text');

    // --- TOOL: IMAGE DESCRIPTOR ---
    document.querySelector('#image-describer-tool button').addEventListener('click', async () => {
        const responseArea = document.querySelector('#image-describer-tool .response-area');
        const imageInput = document.getElementById('image-upload');
        if (imageInput.files.length > 0) {
            responseArea.innerHTML = 'Analyzing Image...';
            const formData = new FormData();
            formData.append('image', imageInput.files[0]);
            try {
                const response = await fetch(`${API_URL}/api/describe-image`, {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const data = await response.json();
                
                // ** THE FIX IS HERE: Also parse image descriptions as Markdown **
                responseArea.innerHTML = marked.parse(data.response);

            } catch (error) {
                console.error("Image Upload Error:", error);
                responseArea.innerHTML = `Error: Could not analyze the image.`;
            }
        } else {
            responseArea.innerHTML = 'Please choose an image file first.';
        }
    });

    // --- TOOL: SPEECH TO TEXT (BROWSER-BASED) ---
    const startSpeechBtn = document.getElementById('start-speech-btn');
    const speechOutput = document.getElementById('speech-output');
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.onstart = () => { speechOutput.innerHTML = 'Listening... Speak now.'; };
        recognition.onresult = (event) => { speechOutput.innerHTML = event.results[0][0].transcript; };
        recognition.onerror = (event) => { speechOutput.innerHTML = 'Error: ' + event.error; };
        startSpeechBtn.addEventListener('click', () => recognition.start());
    } else {
        startSpeechBtn.disabled = true;
        speechOutput.innerHTML = 'Speech recognition is not supported in this browser.';
    }
});