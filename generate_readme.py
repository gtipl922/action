<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI README Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
        }
        .container {
            max-width: 800px;
        }
        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3b82f6;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">

    <div class="container mx-auto bg-white shadow-xl rounded-2xl p-8 md:p-12 transition-all duration-300">
        <div class="text-center mb-10">
            <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-2">AI README Generator</h1>
            <p class="text-gray-600 text-lg">Create a professional README for your project with a single prompt.</p>
        </div>
        
        <!-- API Key Missing Message -->
        <div id="api-key-message" class="hidden bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 rounded-md mb-8" role="alert">
            <p class="font-bold">API Key Missing</p>
            <p>To use this app, you must provide a valid Gemini API key. Get your key from <a href="https://aistudio.google.com/app/apikey" target="_blank" class="font-medium text-yellow-800 underline hover:text-yellow-900 transition duration-200">Google AI Studio</a> and paste it into the 'apiKey' variable in the script section at the bottom of the page.</p>
        </div>

        <!-- Input Section -->
        <div class="mb-8">
            <label for="project-description" class="block text-gray-700 font-semibold mb-2">
                Describe your project:
            </label>
            <textarea id="project-description" rows="6"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200 resize-none placeholder-gray-400"
                placeholder="Example: A full-stack to-do list application built with React, Node.js, and MongoDB. It allows users to create, read, update, and delete tasks."></textarea>
        </div>

        <!-- Action Button -->
        <div class="flex flex-col md:flex-row md:items-center justify-between mb-8">
            <button id="generate-button"
                class="w-full md:w-auto px-6 py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 flex items-center justify-center">
                <span id="button-text">Generate README</span>
                <div id="loader" class="loader ml-3 hidden"></div>
            </button>
        </div>

        <!-- Output Section -->
        <div>
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-2xl font-bold text-gray-800">Generated README</h2>
                <button id="copy-button" class="flex items-center space-x-2 text-blue-600 hover:text-blue-800 transition duration-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M7 9a2 2 0 012-2h6a2 2 0 012 2v6a2 2 0 01-2 2H9a2 2 0 01-2-2V9z" />
                        <path d="M5 3a2 2 0 00-2 2v6a2 2 0 002 2V5h8a2 2 0 00-2-2H5z" />
                    </svg>
                    <span>Copy</span>
                </button>
            </div>
            <div id="output-container" class="bg-gray-50 border border-gray-200 rounded-lg p-6 overflow-x-auto min-h-[300px]">
                <div id="message-box" class="hidden"></div>
                <pre id="output-text" class="whitespace-pre-wrap font-mono text-sm text-gray-800"></pre>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const generateButton = document.getElementById('generate-button');
            const copyButton = document.getElementById('copy-button');
            const projectDescriptionInput = document.getElementById('project-description');
            const outputText = document.getElementById('output-text');
            const loader = document.getElementById('loader');
            const buttonText = document.getElementById('button-text');
            const messageBox = document.getElementById('message-box');
            const apiKeyMessage = document.getElementById('api-key-message');
            
            // API endpoint and key
            const apiKey = "AIzaSyAr7bGN86JdvRmlf9HvjJSDGwCZOkKMQdU"; // <--- PASTE YOUR API KEY HERE
            const apiUrl = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=" + apiKey;

            // Check if API key is provided on page load
            if (!apiKey) {
                apiKeyMessage.classList.remove('hidden');
                generateButton.disabled = true;
            }

            // Handle button click to generate README
            generateButton.addEventListener('click', async () => {
                const projectDescription = projectDescriptionInput.value.trim();
                if (!projectDescription) {
                    showMessage("Please enter a project description.", 'error');
                    return;
                }

                setLoadingState(true);
                outputText.textContent = '';
                showMessage("", 'hide');

                const systemPrompt = "You are a professional README file generator. Your task is to create a comprehensive, well-structured, and visually appealing README.md in Markdown format. The README should include: 1. A placeholder for a professional logo at the top. 2. A title and a concise description. 3. Badges for build status, license, and other relevant metrics. 4. A comprehensive Features section with clear explanations and emojis or icons for each feature. 5. A Technologies Used section with a list of key technologies. 6. Detailed Installation and Usage instructions. 7. A section on Contributing. 8. A clear License section. Use appropriate headings, lists, and code blocks to make the file look polished and professional.";

                const userQuery = `Generate a README file for the following project: ${projectDescription}`;

                const payload = {
                    contents: [{ parts: [{ text: userQuery }] }],
                    systemInstruction: { parts: [{ text: systemPrompt }] },
                };

                let retries = 0;
                const maxRetries = 3;
                let success = false;
                while (retries < maxRetries && !success) {
                    try {
                        const response = await fetch(apiUrl, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });

                        if (!response.ok) {
                             if (response.status === 429) {
                                // Too many requests, retry with exponential backoff
                                await new Promise(resolve => setTimeout(resolve, Math.pow(2, retries) * 1000));
                                retries++;
                                continue;
                            }
                            const errorData = await response.json();
                            throw new Error(errorData.error.message || `API call failed with status: ${response.status}`);
                        }

                        const result = await response.json();
                        const generatedText = result?.candidates?.[0]?.content?.parts?.[0]?.text;
                        if (generatedText) {
                            outputText.textContent = generatedText;
                            success = true;
                        } else {
                            throw new Error("Invalid response format from the API.");
                        }

                    } catch (error) {
                        console.error('API call error:', error);
                        showMessage(`Failed to generate README: ${error.message}`, 'error');
                        setLoadingState(false);
                        return;
                    }
                }
                if (!success) {
                    showMessage("Failed to generate README after multiple retries. Please try again later.", 'error');
                }

                setLoadingState(false);
            });

            // Handle copy button click
            copyButton.addEventListener('click', () => {
                const textToCopy = outputText.textContent;
                if (textToCopy) {
                    // Create a temporary textarea to hold the text
                    const tempTextarea = document.createElement('textarea');
                    tempTextarea.value = textToCopy;
                    document.body.appendChild(tempTextarea);

                    // Select and copy the text
                    tempTextarea.select();
                    document.execCommand('copy');

                    // Clean up
                    document.body.removeChild(tempTextarea);
                    showMessage("README content copied to clipboard!", 'success');
                } else {
                    showMessage("Nothing to copy.", 'error');
                }
            });

            function setLoadingState(isLoading) {
                if (isLoading) {
                    generateButton.disabled = true;
                    loader.classList.remove('hidden');
                    buttonText.classList.add('hidden');
                } else {
                    generateButton.disabled = false;
                    loader.classList.add('hidden');
                    buttonText.classList.remove('hidden');
                }
            }

            function showMessage(message, type) {
                if (message) {
                    messageBox.textContent = message;
                    messageBox.className = 'p-3 rounded-lg text-sm transition-all duration-300 ' + (type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700');
                    messageBox.classList.remove('hidden');
                } else {
                    messageBox.classList.add('hidden');
                }
            }
        });
    </script>

</body>
</html>
