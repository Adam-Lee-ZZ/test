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
        const response = await fetch('/api/getlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input: userInput })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response from the backend
        const data = await response.json();

        // Call the backend function to save the result to the database
        const saveResponse = await fetch('/api/saveToDatabase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ result: data })
        });

        if (!saveResponse.ok) {
            throw new Error(`HTTP error while saving! status: ${saveResponse.status}`);
        }

        alert("Data successfully submitted and saved to the database!");

    } catch (error) {
        console.error('Error:', error);
        alert("An error occurred while submitting the data.");
    }
}

