from flask import Flask, request, render_template, redirect, url_for
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
students = {}
@app.route('/')
def index():
    return render_template('add_student.html')
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    age = request.form.get('age')
    file = request.files.get('photo') 
    if name and age and file and allowed_file(file.filename):
        filename = name + "_" + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        students[name] = {'age': age, 'photo': filename}
        return redirect(url_for('index'))
    return "All fields are required and file must be an image", 400
@app.route('/search_student', methods=['GET', 'POST'])
def search_student():
    if request.method == 'POST':
        name = request.form.get('name')
        student = students.get(name)
        if student:
            return render_template('search_student.html', name=name, age=student['age'], photo=student['photo'])
        return "Student not found", 404
    return render_template('search_student.html', name=None, age=None, photo=None)
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)