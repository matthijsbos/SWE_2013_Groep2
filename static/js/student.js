/*
 * Handles all actions for studentis: showing them the current question and
 * letting them answer it.
 *
 * Note: This can later easily be refactored to also ask for ratings and stuff.
 *       Just alter has_new_question to has_new_action or something...
 */

var has_active_question = false;
var active_question_id;
var query_interval = 1000 * 3; // Every 5 sec
var query_interval_id;

$(function() {
    $("#answerform").submit(submit_answer);
    query_new_question();

	$('#answerform #counter').countdown({until: new Date(),
                                         compact: true,
                                         onExpiry: submit_answer});
    if (!has_active_question)
        query_interval_id = setInterval(query_new_question, query_interval);
});

function query_new_question() {
    if (has_active_question) {
        clearInterval(query_interval_id);
        return;
    }
    $.getJSON("/has_new_question", {},
        function(data) {
            if (data.has_new) {
                show_question(data.question_id, data.question_text,
                    data.time_remaining);
            }
        });
    /* Poll for reviewable questions */
    $.getJSON("/has_new_review", {},
        function(data) {
            if (data.has_new) {
                show_review_button(data.number);
            }
            else {
                show_review_button(0);
            }            
        });

}

function show_review_button(number) {
    console.log("GOT REVIEW", number);
    if (number > 0) {
        $('#reviewform #review-answer').val('You have ('+number+') reviewable answers waiting for you!');
        $('#reviewform').show();
    } else {
        $('#reviewform').hide();
    }

}


function show_question(id, question, time_remaining) {
    console.log("GOT QUESTION", id, question, time_remaining);
    clearInterval(query_interval_id);
    has_active_question = true;
    active_question_id = id;
	var austDay = new Date();
	austDay.setSeconds(austDay.getSeconds() + time_remaining);
    console.log(austDay);
    
    if (time_remaining < 0)
        $('#answerform #counter').hide()
    else{
        $('#answerform #counter').show()
        $('#answerform #counter').countdown('option', {until: austDay,
                                            compact: true,
                                            onExpiry: submit_answer});
    }   

    $('#pleasewait').hide();
    $('#answerform #question').text(question);
    $('#answerform textarea').val('');
    $('#answerform').show();
}

function submit_answer() {
    console.log("SUBMIT");
    has_active_question = false;
    $('#pleasewait').show();
    $('#answerform').hide();

    $.post("/answer", {"questionID": active_question_id,
                       "answerText": $('#answerform textarea').val()});

    query_new_question();
    if (!has_active_question)
        query_interval_id = setInterval(query_new_question, query_interval);
    return false;
}
