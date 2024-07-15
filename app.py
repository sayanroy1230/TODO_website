from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:system@localhost/tododb"
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.today())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
with app.app_context():
    db.create_all()

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method == "POST":
        title=request.form["todotitle"]
        desc=request.form["tododesc"]
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
def todopage():
    if request.method == "POST":
        title=request.form["todotitle"]
        desc=request.form["tododesc"]
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")# get method
    todos = Todo.query.all()
    return render_template("todo.html",todos=todos)

if __name__=="__main__":
    app.run(debug=True,port=27017)
 