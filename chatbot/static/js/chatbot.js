const addUserInputToLog = (inputValue) => {
    const userContainer = document.querySelector("#chat");
    const containerRow = document.createElement("div")
    const containerCol = document.createElement("div")
    const tag = document.createElement("p");
    const text = document.createTextNode("You: " + inputValue);
    containerRow.classList.add("row");
    containerRow.classList.add("no-gutters");
    containerRow.classList.add("justify-content-end");
    containerCol.classList.add("col-7");
    tag.classList.add("bubble-right");
    tag.appendChild(text);
    containerCol.appendChild(tag);
    containerRow.appendChild(containerCol);
    userContainer.appendChild(containerRow);
}

const addBotAnswerToLog = (botResponse) => {
    const botContainer = document.querySelector("#chat");
    const tag = document.createElement("p");
    const containerRow = document.createElement("div");
    const containerCol = document.createElement("div");
    const text = document.createTextNode("ISABOT: " + botResponse);
    containerRow.classList.add("row");
    containerCol.classList.add("col-7");
    tag.classList.add("bubble-left");

    tag.appendChild(text);
    containerCol.appendChild(tag);
    containerRow.appendChild(containerCol);
    botContainer.appendChild(containerRow);
}

const emptyInputField = () => {
    document.querySelector("#user-input").value="";
}

const scrollToBottom = () => {
    const chat = document.querySelector("#chat");
    chat.scrollTop = chat.scrollHeight;
}

async function sendUserInput(event) {
    event.preventDefault();
    const inputValue = document.querySelector("#user-input").value;
    emptyInputField();
    addUserInputToLog(inputValue);
    scrollToBottom();
    const url = window.location.origin + chatterbotUrl;
    await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            "Content-Type": 'application/json',
            "X-CSRFToken": csrftoken
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify({'text': inputValue})
    }).then(response => response.json()).then(data => {
        addBotAnswerToLog(data.text);
        scrollToBottom();
    });
}

const addEventListenerToForm = () => {
    const chatForm = document.querySelector("#chatForm");
    chatForm.addEventListener("submit", sendUserInput, false);
}

addEventListenerToForm();
