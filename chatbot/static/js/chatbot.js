let conversationState = {
    conversationId: "",
    botSessionId: "",
    questionId: 0
}

const setConversationState = (conversationId, botSessionId, questionId) => {
    conversationState.conversationId = conversationId;
    conversationState.botSessionId = botSessionId;
    conversationState.questionId = questionId;
}

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
    document.querySelector("#user-input").value = "";
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
    const url = window.location.origin + postMessageUrl;
    console.log("state before fetch", conversationState)
    await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            "Content-Type": 'application/json',
            "X-CSRFToken": csrftoken
        },
        redirect: 'follow',
        referrerPolicy: 'same-origin',
        body: JSON.stringify(
            {
                "text": inputValue,
                "conversationId": conversationState.conversationId,
                "botSessionId": conversationState.botSessionId,
                "questionId": conversationState.questionId,
            }
        )
    }).then(response => response.json()).then(data => {
        setConversationState(data.conversationId, data.botSessionId, data.questionId);
        addBotAnswerToLog(data.text);
        scrollToBottom();
        console.log("state after post: ", conversationState);
    }).catch((error) => {
        console.error(error);
    });
}

function startBotCommunication() {
    console.log("in start")
    const url = window.location.origin + getConversationUrl;
    console.log(window.location.origin + getConversationUrl)
    fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
    }).then(response => response.json()).then(data => {
        setConversationState(data.conversationId, data.botSessionId, data.questionId);
        addBotAnswerToLog(data.text);
        scrollToBottom();
        console.log("state after first contact: ", conversationState);
    }).catch((error) => {
        console.error(error);
    });
}

const addEventListenerToForm = () => {
    const chatForm = document.querySelector("#chatForm");
    chatForm.addEventListener("submit", sendUserInput, false);
}

window.onload = (event) => {
    console.log('page is fully loaded');
    addEventListenerToForm();
    startBotCommunication();
};
