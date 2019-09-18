let userAnswerStatus = false;
let userQuestionCommentStatus = false;
let userAnswerCommentStatus = false;

let userAnswer = function () {
    let getUserAnswer = document.querySelectorAll(".tr-user_answers");
    if (userAnswerStatus === false) {
        for (let i = 0; i < getUserAnswer.length; ++i){
            getUserAnswer[i].style.display = "block";
            userAnswerStatus = true;
        }
    } else {
        for (let i = 0; i < getUserAnswer.length; ++i){
            getUserAnswer[i].style.display = "none";
            userAnswerStatus = false;
        }
    }
};

let userQuestionComment = function () {
    let getUserQuestionComment = document.querySelectorAll(".tr-user-question-comment");
    if (userQuestionCommentStatus === false) {
        for (let i = 0; i < getUserQuestionComment.length; ++i){
            getUserQuestionComment[i].style.display = "block";
            userQuestionCommentStatus = true;
        }
    } else {
        for (let i = 0; i < getUserQuestionComment.length; ++i){
            getUserQuestionComment[i].style.display = "none";
            userQuestionCommentStatus = false;
        }
    }
};

let userAnswerComment = function () {
    let getUserAnswerComment = document.querySelectorAll(".tr-user-answer-comment");
    if (userAnswerCommentStatus === false) {
        for (let i = 0; i < getUserAnswerComment.length; ++i){
            getUserAnswerComment[i].style.display = "block";
            userAnswerCommentStatus = true;
        }
    } else {
        for (let i = 0; i < getUserAnswerComment.length; ++i){
            getUserAnswerComment[i].style.display = "none";
            userAnswerCommentStatus = false;
        }
    }
};