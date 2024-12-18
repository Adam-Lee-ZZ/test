function submitData() {
    alert("YYYYYYY")
    const inputElement = document.getElementById("inputField");
    if (!inputElement) {
        console.error("Input field not found!");
        return;
    }
  
    const inputText = inputElement.value.trim();
    if (inputText === "") {
        alert("Please enter some text.");
        return;
    }
  
    // 發送 POST 請求
    fetch('https://nice-plant-087bc3400.4.azurestaticapps.net/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ inputData: inputText })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // 假設返回的是 JSON
    })
    .then(data => {
        // 在這裡跳轉到新的頁面
        window.location.href = "https://you.tube.com"; // 修改為你希望跳轉的頁面 URL
    })
    .catch(error => {
        alert("An error occurred: " + error.message);
    });
  }
  