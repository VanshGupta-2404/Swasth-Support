const express = require('express');
const bodyParser = require('body-parser');
const { GoogleGenerativeAI } = require('@google/generative-ai');

const app = express();
const port = 2000; // Adjust port as needed

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Initialize your Generative AI instance
const apiKey = 'AIzaSyAwqVXD03Dtm-r2FPaRnc-VHNR276zHiDQ'; // Replace with your actual API key
const genAI = new GoogleGenerativeAI(apiKey);

// Define your generative model
const model = genAI.getGenerativeModel({
    model: 'gemini-1.5-flash',
    systemInstruction: 'Your system instruction here'
});

// Example route handling POST request to /api/chat
app.post('/api/chat', async (req, res) => {
    const userMessage = req.body.message;

    try {
        // Example: fetch response from generative AI or process request
        const botResponse = await model.sendMessage(userMessage);

        // Send back response to client
        res.json({ response: botResponse });
    } catch (error) {
        console.error('Error in /api/chat:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Start server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
