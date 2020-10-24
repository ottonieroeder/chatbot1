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

const emptyChatContainer = () => {
    const container = document.querySelector("#chat");
    container.textContent = '';
}

const scrollToBottom = () => {
    const chat = document.querySelector("#chat");
    chat.scrollTop = chat.scrollHeight;
}

const scrollToChat = ()  => {
    //  emptyChatContainer();
    // startBotCommunication();
    const target = document.querySelector("#isabot");
    target.scrollIntoView({ block: "center", behavior: "smooth" });
}

const hideVideoModal = ()  => {
    const target = document.querySelector("#isa-video-modal");
    const targetFixedVideo = document.querySelector("#isa-video-fixed");
    target.classList.add("hide-video");
    targetFixedVideo.classList.add("show-video");
}

const hideFixedVideo = ()  => {
    const target = document.querySelector("#isa-video-fixed");
    target.classList.remove("show-video");
}

const addClickEventListenerToSessionButton = () => {
    console.log("added listener")
    document.querySelector("#session-btn").addEventListener("click", scrollToChat);
    document.querySelector("#session-btn-mobile").addEventListener("click", scrollToChat);
}

const addClickEventListenerToVideoContainer = () => {
    document.querySelector("#red-dot").addEventListener("click", hideVideoModal);
    document.querySelector("#red-dot-fixed").addEventListener("click", hideFixedVideo);
}

async function sendUserInput(event) {
    event.preventDefault();
    const inputValue = document.querySelector("#user-input").value;
    emptyInputField();
    addUserInputToLog(inputValue);
    scrollToBottom();
    const url = window.location.origin + postMessageUrl;
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
    }).catch((error) => {
        console.error(error);
    });
}

function startBotCommunication() {
    const url = window.location.origin + getConversationUrl;
    fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
    }).then(response => response.json()).then(data => {
        setConversationState(data.conversationId, data.botSessionId, data.questionId);
        addBotAnswerToLog(data.text);
        scrollToBottom();
    }).catch((error) => {
        console.error(error);
    });
}

const addEventListenerToForm = () => {
    const chatForm = document.querySelector("#chat-form");
    chatForm.addEventListener("submit", sendUserInput, false);
}


window.onload = (event) => {
    addEventListenerToForm();
    addClickEventListenerToSessionButton();
    addClickEventListenerToVideoContainer();
    startBotCommunication();
};