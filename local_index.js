const inputData = [];

main();

async function main() {
    try {
        await submitData();
    } catch (error) {
        console.error("Error in main function:", error);
    }
}

async function submitData() {
    // Get user input from a text input field with id 'userInput'
    const userInput = document.getElementById('userInput').value;

    if (!userInput) {
        alert("Please enter some text before submitting.");
        return;
    }

    try {
        // Send the user input to the backend API endpoint
        const response = await fetch('/api/function_app', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ inputData: userInput })  // Ensure this matches the key in Python
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response from the backend
        const data = await response.json();
        console.log('Response from server:', data); // Handle the server response here

    } catch (error) {
        console.error('Error:', error);
        alert("An error occurred while submitting the data.");
    }
}
