from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import random
from sqlalchemy.sql.expression import func




app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()

class Questions(db.Model):
    __tablename__ = "Questions"
    q_id = db.Column(db.Integer(), primary_key=True)
    question = db.Column(db.String(1000),unique=True)
    op_1 = db.Column(db.String(100))
    op_2 = db.Column(db.String(100))
    op_3 = db.Column(db.String(100))
    op_4 = db.Column(db.String(100))
    ans = db.Column(db.String(100))

    def __init__(self,q_id,question,op_1,op_2,op_3,op_4,ans):
        self.q_id = q_id
        self.question = question
        self.op_1 = op_1
        self.op_2 = op_2
        self.op_3 = op_3
        self.op_4 = op_4
        self.ans = ans


score = 0
ques_dis = 10

@app.route("/",methods=["POST","GET"])
def quiz():
    if request.method == "POST":
        global ques_dis
        global score
        ques_dis = ques_dis+1
        row_count = db.session.query(Questions).count()
        correct_ans = request.form["correct_ans"]

        if correct_ans == request.form["option"]:
            score = score+1
        
        if ques_dis== 10:
            print("Your Score:",score)
            
        
        shuffled_question = db.session.query(Questions).order_by(func.random())
        print(shuffled_question.question) 
        return render_template("quiz.html",shuffled_question=shuffled_question)

@app.route("/admin",methods=["POST","GET"])
def admin():
    if request.method == "POST":
        if not request.form["question"] or not request.form["op_1"] or not request.form ["op_2"] or not request.form["op_3"] or not request.form["op_4"]or not request.form["answer"]:
            print("Please enter all the fields")

        else:
            rows = db.session.query(Questions).count()
            mcq = Questions(request.form["q_id"],request.form["question"],request.form["op_1"],request.form["op_2"],request.form["op_3"],request.form["op_4"],request.form["ans"])
            db.session.add(mcq)
            db.session.commit()
            print("Question added succesfully")
            return redirect("/admin")

    ques_list = Questions.query.all()
    return render_template("admin.html", ques_list=ques_list)

@app.route("/update")
def update():
        new_question = request.form.get("new_question")
        newOp_1 = request.form.get("newOp_1")
        newOp_2 = request.form.get("newOp_2")
        newOp_3 = request.form.get("newOp_3")
        newOp_4 = request.form.get("newOp_4")
        newAns = request.form.get("newAns")
        
        old_question = request.form.get("old_question")
        mcq = Questions.query.filter_by(question=old_question).first()
        if request.form["new_question"]:
            mcq.question=new_question

        if request.form["new_option1"]:
            mcq.op_1=newOp_1

        if request.form["new_option2"]:
            mcq.op_2 =newOp_2

        if request.form["new_option3"]:
            mcq.op_3 =newOp_3

        if request.form["new_option4"]:
            mcq.op_4=newOp_4

        if request.form["new_answer"]:
            mcq.ans=newAns

        db.session.commit()
        return redirect("/admin")

@app.route("/delete",methods=["POST"], )
def delete():
        question = request.form.get("del_question")
        mcq = Questions.query.filter_by(question=question).first()
        db.session.delete(mcq)
        db.session.commit()
        return redirect("/admin")

if __name__ == "__main__":
        app.run(debug=True)



