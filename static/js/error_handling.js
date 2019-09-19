let logMessage = document.querySelector(".log-message");

let errorHandler = function () {
    if (logMessage.innerText === 'You are not logged in') {
        alert(logMessage.innerText);
    }
};

let loginHandler = function () {

};