const addUserInputToLog = (inputValue) => {
    const userContainer = document.querySelector("#chat");
    var containerRow = document.createElement("div")
    var containerCol = document.createElement("div")
    var tag = document.createElement("p");
    var text = document.createTextNode(inputValue);
    containerRow.classList.add("row")
    containerRow.classList.add("no-gutters")
    containerRow.classList.add("justify-content-end")
    containerCol.classList.add("col-4")
    tag.classList.add("bubble-right");

    tag.appendChild(text);
    containerCol.appendChild(tag);
    containerRow.appendChild(containerCol);
    userContainer.appendChild(containerRow);
    console.log(userContainer)
}

const addBotAnswerToLog = (botResponse) => {
    const botContainer = document.querySelector("#chat");
    var tag = document.createElement("p");
    var containerRow = document.createElement("div")
    var containerCol = document.createElement("div")
    var text = document.createTextNode(botResponse);
    containerRow.classList.add("row");
    containerCol.classList.add("col-4");
    tag.classList.add("bubble-left");

    tag.appendChild(text);
    containerCol.appendChild(tag);
    containerRow.appendChild(containerCol);
    botContainer.appendChild(containerRow);
}

const emptyInputField = () => {
    document.querySelector("#user-input").value="";
}

async function sendUserInput(event) {
    event.preventDefault();
    const inputValue = document.querySelector("#user-input").value;
    emptyInputField()
    addUserInputToLog(inputValue)
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
        addBotAnswerToLog(data.text)
    });
}

const addEventListenerToForm = () => {
    const chatForm = document.querySelector("#chatForm");
    chatForm.addEventListener("submit", sendUserInput, false);
}

addEventListenerToForm();
