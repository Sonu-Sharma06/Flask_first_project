from flask import Flask, render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# create a simple flask application

#initializing flask class
app=Flask(__name__)

#databse setup
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


#making database schema using sqlalchemy
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"


# 1. flask app url routing

@app.route("/",methods=["GET","POST"])
def welcome():
    if request.method=="POST":
        title=request.form.get("title")
        description=request.form.get("descrip")
        todo=Todo(title=title,desc=description)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()

    return render_template('index.html',alltodo=alltodo)

@app.route("/update/<int:slno>",methods=["GET","POST"])
def update(slno):
    if request.method=="POST":
       title=request.form.get("title")
       description=request.form.get("descrip")
       todo=Todo.query.filter_by(sno=slno).first()
       todo.title=title
       todo.desc=description
       db.session.add(todo)
       db.session.commit()
       return redirect("/")

    todo=Todo.query.filter_by(sno=slno).first()
    return render_template('update.html',todo=todo)
#2. flask variable rule

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# 3. flask html render

@app.route("/form",methods=["GET","POST"])
def new_form():
    if request.method=="GET":
        return render_template("form.html")
    else:
        maths=int(request.form['maths'])
        scie=int(request.form['science'])
        hist=int(request.form['history'])

        avg_marks=(maths+scie+hist)/3
        
        return render_template('form.html',score=avg_marks)
    

if __name__=="__main__":
    with app.app_context():
      db.create_all()
    app.run(debug=True) #url = localhost  port=5000 by default if not given
