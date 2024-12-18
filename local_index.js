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
    try {
        const response = await fetch('/api/src/functions');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const reData = await response.json();
        const reInput = reData.inputField;
        console.log("Received data:", reInput);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}
