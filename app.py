from flask import Flask,render_template,request
from datetime import datetime

from werkzeug.utils import redirect

from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)

app.config ["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///user.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String(200),nullable=False)
    email = db.Column (db.String(200),nullable=False)
    phone_number = db.Column (db.String(200),nullable=False)
    creted_at = db.Column (db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' %self.id


@app.route('/',methods =['POST','GET'])
def home():
  if request.method =='POST':
    user_name = request.form["fullname"]
    user_email = request.form["email"]
    user_number = request.form["number"]
    new_user = Users(full_name=user_name,email=user_email,phone_number=user_number)
    try:
      db.session.add(new_user)
      db.session.commit()
      return redirect("/")
    except:
      return "Error posting your information"
  else:
    users = Users.query.order_by (Users.creted_at).all ()
    return render_template("index.html",users=users)

@app.route('/delete/<int:id>')
def delete(id):
   user_to_delete = Users.query.get_or_404(id)
   try:
     db.session.delete(user_to_delete)
     db.session.commit()
     return redirect("/")
   except:
      return "Error in deleting your data"

@app.route('/update/<int:id>',methods = ['POST','GET'])
def update(id):
   user = Users.query.get_or_404(id)
   if request.method == "POST":
     user.full_name = request.form["fullname"]
     user.email = request.form["email"]
     user.phone_number = request.form["number"]
     try:
       db.session.commit()
       return redirect('/')
     except:
       "Error in updating your data"
   else:
      return render_template('update.html',user=user)
if __name__ == "__main__":
  app.run(debug=True)