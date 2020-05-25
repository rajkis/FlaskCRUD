# Import packages dependent on this app
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create an instance
app = Flask(__name__)

#Configure and create the SQLAlchemy object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Define the model using the Model class provided by that object
class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    qty = db.Column(db.Integer, nullable=True)
    unit = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    def __repr__(self):
        return '<Grocery %r>' % self.name

#specify the URL for the function using decorators
#captures name attribute value of a form
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        new_stuff = Grocery(name=name)
        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect ('/')
        except:
            return "There was a problem adding new stuff!"

    else:
        groceries = Grocery.query.order_by(Grocery.created_at).all()
        return render_template('index.html', groceries=groceries)

#Function for update record
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    grocery = Grocery.query.get_or_404(id)

    if request.method == 'POST':
        grocery.name = request.form["name"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem updating record!"
    
    else:
        title = "Update Data"
        return render_template("update.html", title=title, grocery=grocery)
        

#Function for delete record
@app.route("/delete/<int:id>")
def delete(id):
    grocery = Grocery.query.get_or_404(id)

    try:
        db.session.delete(grocery)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deletinig record!"


#if the script is run directly from the Python interpreter
if __name__ == '__main__':
    app.run(debug=True)

