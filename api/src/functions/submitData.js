module.exports
document.addEventListener('DOMContentLoaded', () => {
    const inputElement = document.getElementById("inputField");
    const submitButton = document.getElementById("submitButton");

    if (!inputElement || !submitButton) {
        console.error("Input field or button not found!");
        return;
    }

    submitButton.addEventListener('click', async () => {
        const inputText = inputElement.value.trim();

        if (inputText === "") {
            alert("Please enter some text.");
            return;
        }

        try {
            // 发送 POST 请求到 Azure Functions API
            const response = await fetch('/api/src/functions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ inputData: inputText })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("API Response:", data);

            // 跳转到新的页面
            window.location.href = "/submit"; // 修改为你实际希望跳转的页面路径
        } catch (error) {
            alert("An error occurred: " + error.message);
            console.error("Error in POST request:", error);
        }
    });
});
