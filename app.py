from flask import Flask,json, request, render_template, redirect, url_for, flash, session, send_file
from pymongo import MongoClient
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import bcrypt

app = Flask(__name__)
app.secret_key = "R0t7K8e!A3tBz4y#E6sW9vZ2yP5s&Y8v@J3kL7nM2oP4rS6uV"
client = MongoClient('localhost', 27017)
db = client['facultydb']
users_collection = db['faculty']

def check_pass(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('signUp'))

        existing_user = users_collection.find_one({'email':email})
        if existing_user:
            flash('Email already exists. Please choose a different email.', 'error')
            return redirect(url_for('signUp'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = {
            'name': name,
            'email': email,
            'password': hashed_password
        }
        users_collection.insert_one(new_user)

        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signUp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email and password are required.', 'error')
            return redirect(url_for('login'))

        user = users_collection.find_one({'email':email})
        if user and check_pass(user['password'], password):
            session['name'] = user['name']
            session['email'] = user['email']
            session['user_id'] = str(user['_id'])
            return redirect(url_for('generate'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if 'name' in session:
        if request.method == 'POST':
            course_name = request.form.get('course-name')
            course_code = request.form.get('course-code')
            questions = request.form.get('question-paper')

            if not course_name or not course_code or not questions:
                flash('All fields are required.', 'error')
                return redirect(url_for('generate'))

            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)

            logo_path = 'static/adamas.jpg'
            c.drawImage(logo_path, 45, 705, width=100, height=100)

            university_name = "Adamas University"
            university_address = "Jagannathpur, Barasat-Barrackpore Road, Kol- 700124"
            c.setFont("Helvetica", 12)
            c.drawString(180, 740, university_address)
            c.drawString(180, 760, university_name)

            exam_heading = "End Semester Exam - June-July 2024"
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 700, exam_heading)

            c.setFont("Helvetica", 12)
            c.drawString(50, 680, f"Course Name: {course_name}")
            c.drawString(50, 665, f"Course Code: {course_code}")
            c.drawString(50, 640, "Questions:")
            text = c.beginText(50, 620)
            text.setFont("Helvetica", 12)
            for line in questions.split('\n'):
                text.textLine(line)
            c.drawText(text)

            c.showPage()
            c.save()
            buffer.seek(0)

            return send_file(buffer, as_attachment=True, download_name='question_paper.pdf', mimetype='application/pdf')

        return render_template('final.html')
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
