function selectQuestion(questionNumber) {

    var questionNumbers = document.getElementById("question-numbers").children;

    for (var i = 0; i < questionNumbers.length; i++) {
        questionNumbers[i].classList.remove("selected");
    }

    var questionNumberElement = document.getElementById("question-" + questionNumber);
    questionNumberElement.classList.add("selected");

    var questionContainers = document.getElementsByClassName("question-container");

    for (var i = 0; i < questionContainers.length; i++) {
        questionContainers[i].style.display = "none";
    }

    var questionContainer = document.getElementById("question-container-" + questionNumber);
    questionContainer.style.display = "block";

    var questionApprovalCommentContainers = document.getElementsByClassName("question-approval-comment-container");

    for (var i = 0; i < questionApprovalCommentContainers.length; i++) {
        questionApprovalCommentContainers[i].style.display = "none";
    }

    var questionApprovalCommentContainer = document.getElementById("question-approval-comment-container-" + questionNumber);
    questionApprovalCommentContainer.style.display = "block";

}
