/*
 * Handles all actions for studentis: showing them the current question and
 * letting them answer it.
 *
 * Note: This can later easily be refactored to also ask for ratings and stuff.
 *       Just alter has_new_question to has_new_action or something...
 */

var has_active_question = false;
var active_question_id;
var query_interval = 1000 * 5; // Every 5 sec
var query_interval_id;
var time_delta;
var submit_interval_id;
var time_check_interval = 5000;

$(function() {
    $("#answerform").submit(submit_answer);
    query_new_question();

	$('#answerform #counter').countdown({until: new Date(),
                                         compact: true,
                                         onExpiry: check_submit_answer});
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
                    data.time_remaining,data.question_time);
            }
        });
}

function show_question(id, question, time_remaining, question_time) {
    console.log("GOT QUESTION", id, question, time_remaining);

    clearInterval(query_interval_id);
    submit_interval_id = setInterval(check_remaining_time,time_check_interval)

    has_active_question = true;
    active_question_id = id;
    time_delta = question_time;

	var austDay = new Date();
	austDay.setSeconds(austDay.getSeconds() + time_remaining);
    console.log(austDay);
	$('#answerform #counter').countdown('option', {until: austDay,
                                         compact: true,
                                         onExpiry: check_submit_answer});
    $('#pleasewait').hide();
    $('#answerform #question').text(question);
    $('#answerform textarea').val('');
    $('#answerform').show();
}

function check_submit_answer(){
    console.log("Check SUBMIT");
    if (!check_remaining_time())
    {
            submit_answer();
    }
}

function check_remaining_time(){
    if(!has_active_question)
    {
        return false;
    }

    var res = false;
    $.getJSON("/question_remaining_time", {questionID:active_question_id},
        function(data) {
            if (data.still_available)
            {
                if (data.question_time > time_delta)
                {
                    var austDay = new Date();
                    austDay.setSeconds(austDay.getSeconds() + data.time_remaining);
                    console.log(austDay);

                    $('#answerform #counter').countdown('option',
                                                     {until: austDay});

                    pupub_div('#answerform #prolongedText')

                    time_delta = data.question_time;
                    res = true;
                }
            }
            else
            {
                if(data.question_deleted)
                {
                    show_query_screen();
                    activate_new_question_query();                
                    popup_div('#questionWasDeleted',5000)
                }
            }
            res = false;
        });

    return res;
}

function popup_div(div,time)
{
    time = (typeof time === "undefined") ? 1500 : time;
    $(div).show();
    $(div).hide(time);
}

function show_query_screen()
{
    clearInterval(submit_interval_id);
    has_active_question = false;
    $('#pleasewait').show();
    $('#answerform').hide();
}

function activate_new_question_query()
{
    query_new_question();
    if (!has_active_question)
        query_interval_id = setInterval(query_new_question, query_interval);
}

function submit_answer() {
    console.log("SUBMIT");
    show_query_screen();

    $.post("/answer", {"questionID": active_question_id,
                       "answerText": $('#answerform textarea').val()});

    activate_new_question_query()
    return false;
}
