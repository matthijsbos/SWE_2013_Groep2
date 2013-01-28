/*
 * Handles all actions for studentis: showing them the current question and
 * letting them answer it.
 *
 * Note: This can later easily be refactored to also ask for ratings and stuff.
 *       Just alter has_new_question to has_new_action or something...
 */

var query_interval = 1000 * 5; // Every 5 sec
var query_interval_id;
var submit_interval_id= new Array();
var time_check_interval = 5000;

$(function() {    
    query_new_question()
    query_interval_id = setInterval(query_new_question, query_interval);    
});

function query_new_question() {    
    $.getJSON("/has_new_question", {},
        function(data) {          
            if (data.has_new) {
                for (var i=0;i<data.len;i++){
                    if($('#answerform'+data.questions[i].question_id).length == 0) {
                        show_question(data.questions[i].question_id, data.questions[i].question_text,
                            data.questions[i].time_remaining, data.questions[i].question_time, 
                            data.questions[i].answer);
                    }
                }
            }
            else {
                /* Poll for reviewable questions */
                $.getJSON("/has_new_review", {},
                    function(data) {
                        if (data.has_new) {
                            show_review_button();
                        }
                        else {
                            hide_review_button();
                        }            
                    });
            }
        });
}

function show_review_button() {
    console.log("GOT REVIEW");
    $('#reviewform #review-answer').val('You have a reviewable answer waiting for you!');
    $('#reviewform').show();
}

function hide_review_button() {
    $('#reviewform').hide();
}

function toggleQ(id){
    if(document.getElementById('answer'+id).style.display == 'none')
        document.getElementById('answer'+id).style.display = ''
    else
        document.getElementById('answer'+id).style.display = 'none'
}
function show_question(id, question, time_remaining, question_time, answer) {
    console.log("GOT QUESTION", id, question, time_remaining);
    submit_interval_id[id] = setInterval(function(){
        check_remaining_time(id, question_time)
    },time_check_interval)
    
    var austDay = new Date();
    austDay.setSeconds(austDay.getSeconds() + time_remaining);
    console.log(austDay);
    $('#questions').append('<form id="answerform'+id+'" method="post" style="display:none;">\
        <br>\
        <div class="accordion-group no-border" id="questionArea'+id+'" class="questionArea">\
            <div id="question'+id+'" class="question accordion-header"></div>\
            <div id="answer'+id+'"  class="accordion-body collapse">\
            <div class="accordion-inner"><textarea name="answerText" cols=50 rows=5></textarea>\
            <br>\
            <button class="btn btn-info" onclick="submit_answer('+id+'); return false;" value="submit answer">submit answer</button>\
            <div id="submitted'+id+'" style="display:none" class="submitted alert alert-success"><button type="button" class="close close-submitted" onclick="document.getElementById(\'submitted'+id+'\').style.display = \'none\';">&times;</button><b>Answer saved!</b><br/></div>\
            <div id="ranking'+id+'"><a href="/choicelobby?question_id='+id+'" >rank it!</a></div>\
            </div></div>\
            <div id="counter'+id+'" class="countdowntimesmall"></div>\
            <div id="prolongedText'+id+'" style="display: none;">Question has been prolonged</div>\
        </div>\
    </form>');
    
    if (question_time != 0) {
        $('#answerform'+id+' #counter'+id).countdown({
            until: austDay,
            compact: true,
            onExpiry: function(){
				check_submit_answer(id, question_time)
				$.post('/start_review', {'question_id': id});
			}        
        });
    }
    
    $('#pleasewait').hide();
    $('#answerform'+id+' #question'+id).html("<a class='accordion-toggle' onclick='collapse_timer("+id+");' data-toggle='collapse' data-parent='#questions' href='#answer"+id+"'>"+question+"</a>");
    $('#answerform'+id+' textarea').val(answer);
    if (answer == '') {
        $('#ranking'+id).hide();
    }
    $('#answerform'+id).show();
}

function check_submit_answer(id, question_time){
    console.log("Check SUBMIT" + id);
    if (!check_remaining_time(id, question_time))
    {
        submit_answer(id);
    }
    $('#answerform'+id).remove();
    clearInterval(submit_interval_id[id]);
    if ( $('#questions').is(':empty') )
    {
        $('#pleasewait').show();
    }
}

function check_remaining_time(id, time_delta){
    var res = false;
    $.getJSON("/question_remaining_time", {
        questionID:id
    },
    function(data) {
        res = false;
        if (data.still_available)
        {
            if (data.question_time != time_delta)
            {
                var austDay = new Date();
                austDay.setSeconds(austDay.getSeconds() + data.time_remaining);
                console.log(austDay);

                $('#answerform'+id+' #counter'+id).countdown('option',
                {
                    until: austDay
                });
                if (data.question_time > time_delta)
                    popup_div('#answerform'+id+' #prolongedText'+id)

                time_delta = data.question_time;
                submit_interval_id[id] = setInterval(function(){
                    check_remaining_time(id, time_delta)
                },time_check_interval)
                res = true;
            }
        }
        else
        {            
            if(data.question_deleted)
            {
                if ( $('#questions').is(':empty') )
                {
                    $('#pleasewait').show();
                }
                $('#answerform'+id).remove();      
                clearInterval(submit_interval_id[id]);
                popup_div('#questionWasDeleted',5000)
            }
        }
    });

    return res;
}

function popup_div(div,time) {
    time = (typeof time === "undefined") ? 1500 : time;
    $(div).show();
    $(div).delay(time).hide(1);
}

function submit_answer(id) {
    console.log("SUBMIT");
    document.getElementById('submitted'+id).style.display = ""
    $('#ranking'+id).show();
    $('#submitted'+id).delay(5000).hide("slow")
    $.post("/answer", {
        "questionID": id,
        "answerText": $('#answerform'+id+' textarea').val()
    });            
}

function collapse_timer(id){
    if ($('#answer'+id).hasClass("in") && $('#answer'+id).height() == 189){
        $('#counter'+id).addClass('countdowntimesmall');
        $('#counter'+id).removeClass('countdowntime');
    } else if($('#answer'+id).height() == 0){
        $('#counter'+id).addClass('countdowntime');
        $('#counter'+id).removeClass('countdowntimesmall');
    }
}
