document.addEventListener('DOMContentLoaded', function() {
  // get the form, submit button, and answer count elements
  var form = document.querySelector('#question-form');
  var submitButton = document.querySelector('#finish_button');
  var answerCount = document.querySelector('#answer-count');

  // add event listener for changes to form inputs
  form.addEventListener('change', function() {
    // get all the questions and their answer options
    var questions = document.querySelectorAll('.col');
    var numQuestions = questions.length;
    var numAnswered = 0;

    // iterate over each question and count how many answer options are selected
    for (var i = 0; i < numQuestions; i++) {
      var question = questions[i];
      var answerOptions = question.querySelectorAll('.answer-option');
      var numSelected = 0;
      for (var j = 0; j < answerOptions.length; j++) {
        if (answerOptions[j].checked) {
          numSelected++;
        }
      }
      if (numSelected === 1) {
        numAnswered++;
      }
    }

    // update the answer count element
    answerCount.innerHTML = "A total of " + numAnswered + " possible answers were marked";

    // show or hide the submit button based on the number of answered questions
    if (numAnswered === numQuestions) {
      submitButton.classList.remove('d-none');
    } else {
      submitButton.classList.add('d-none');
    }
  });
});

var timeleft = 600; // 10 minutes in seconds
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
		document.getElementById("finish_button").click(); // Simulate clicking the Finish button when the time is up
	  }
	}, 1000);