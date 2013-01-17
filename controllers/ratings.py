from models.ratings import AnswerRating
from dbconnection import session

class AssignRatings():
    def __init__(self, answer_id):
        self.answer = AnswerRating.by_id(answer_id)
        fsession['assignrating'] = str(answer_id)
    
    @staticmethod
    def assign(request):
        for rating_id in request.form.getlist('ratings'):
            AnswerRating.add_answerrating(fsession['assignrating'], rating_id)
              
    def render(self):
        return render_template('ratings.html', answer=self.answer,
                               ratings=Rating.get_all())