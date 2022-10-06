from crypt import methods


from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"

@app.route('/',methods = ['GET','POST'])
def hello_world():
    if request.method == "POST":
        tasktitle = request.form['title']
        taskdescription = request.form['description']
        if tasktitle == "" and taskdescription == "":
            return redirect('/')
        else:
            todo = Todo( title = tasktitle , desc = taskdescription )
            db.session.add(todo)
            db.session.commit()
            alltodo = Todo.query.all()
            print(alltodo)
            return render_template('index.html',alltodo=alltodo)
    elif request.method == "GET":
        alltodo = Todo.query.all()
        print(alltodo)
        return render_template('index.html',alltodo=alltodo)
    

@app.route('/home')
def products():
    return redirect('/')

@app.route('/addanothertask')
def addtask():
    return redirect('/')


@app.route('/delete/<int:sno>')
def delete(sno):
    print(sno)
    task = Todo.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    print(task)
    alltodo = Todo.query.filter_by().order_by(desc(Todo.date_created))
    return render_template('mytask.html',alltodo = alltodo)


@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == "GET":
        task = Todo.query.filter_by(sno=sno).first()
        return render_template('update.html',task = task)
    elif request.method == "POST":
        print("in post request user")
        tasktitle = request.form['title']
        taskdescription = request.form['description']
        todotask = Todo.query.filter_by(sno=sno).first()
        todotask.title = tasktitle
        todotask.desc = taskdescription
      
        db.session.commit()
        return redirect('/')
@app.route('/mytask',methods=['GET'])
def mytasks():
    alltodo = Todo.query.filter_by().order_by(desc(Todo.date_created))
    return render_template('mytask.html',alltodo = alltodo)

@app.route('/backhome',methods=['GET'])
def backhome():
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)