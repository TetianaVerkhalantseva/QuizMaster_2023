function onRemoveQuizClick(redirect_link) {

    if (confirm("Er du sikker på at du vil slette denne quizen?"))
        window.location.href = redirect_link;

}


function onRemoveQuestionClick(redirect_link) {

    if (confirm("Er du sikker på at du vil slette dette spørsmålet?"))
        window.location.href = redirect_link;

}
