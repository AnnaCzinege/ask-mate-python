let errorHandler = function () {
    let logMessage = document.querySelector(".log-message");
    if (logMessage.innerText === 'You are not logged in') {
        alert(logMessage.innerText);
    }
};