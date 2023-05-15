document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("#question-form");
  const submitButton = document.querySelector("#finish_button");
  const answerCount = document.querySelector("#answer-count");

  form.addEventListener("change", function () {
    const questions = document.querySelectorAll(".col");
    const numQuestions = questions.length;
    let numAnswered = 0;

    for (let i = 0; i < numQuestions; i++) {
      const question = questions[i];
      const answerOptions = question.querySelectorAll(".answer-option");
      let numSelected = 0;
      for (let j = 0; j < answerOptions.length; j++) {
        if (answerOptions[j].checked) {
          numSelected++;
        }
      }
      if (numSelected === 1) {
        numAnswered++;
      }
    }

    answerCount.innerHTML =
      "A total of " + numAnswered + " possible answers were marked";

    if (numAnswered === numQuestions) {
      submitButton.classList.remove("d-none");
    } else {
      submitButton.classList.add("d-none");
    }
  });
});

var timeleft = 900; // 15 minutes in seconds
	var downloadTimer = setInterval(function(){
	  timeleft--;
	  var minutes = Math.floor(timeleft / 60);
	  var seconds = timeleft % 60;
	  if (seconds < 10) {
		seconds = "0" + seconds;
	  }
	  document.getElementById("timer").innerHTML = minutes + ":" + seconds;
	  if(timeleft <= 0){
      clearInterval(downloadTimer);
      window.location.href = "/results"; 
    }
	}, 1000);