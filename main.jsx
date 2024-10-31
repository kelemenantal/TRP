const OpenAI = require("openai");
const fs = require("fs").promises;  // Node.js module to handle file reading
const path = require("path");  // Node.js module to handle paths

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,  // Ensure the API key is set as an environment variable
});

(async () => {
    try {
        // Construct the path to the .txt file relative to your project root
        const filePath = path.join(__dirname, 'files', 'TVSZ.txt');

        // Read the content of the .txt file
        const fileContent = await fs.readFile(filePath, 'utf-8');  // Directly read text content

        // Pass the file content into the OpenAI API request
        const completion = await openai.chat.completions.create({
            model: "gpt-4o",
            messages: [
                { role: "system", content: "You are a helpful assistant who reads the provided content and answers questions about it." },
                {
                    role: "user",
                    content: `Here is the content of the file:\n\n${fileContent}\n\nHogyan tudom meghatározni a súlyozott tanulmányi átlagomat?`,  // Provide the file content in the user input
                },
            ],
        });

        // Output the result
        console.log(completion.choices[0].message.content);
    } catch (error) {
        console.error("Error reading the file or making the request:", error);
    }
})();