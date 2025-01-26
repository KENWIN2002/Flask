from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        phone = request.form['phone']

        new_student = Student(name=name, dob=dob, phone=phone)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('add_student'))

    return render_template('add_student.html')

@app.route('/search_student', methods=['GET', 'POST'])
def search_student():
    student = None
    if request.method == 'POST':
        name = request.form['name']
        student = Student.query.filter_by(name=name).first()

    return render_template('search_student.html', student=student)

if __name__ == '__main__':
    app.run() 