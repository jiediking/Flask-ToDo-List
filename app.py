from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    due_time = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    inspector = db.inspect(db.engine)
    cols = [c['name'] for c in inspector.get_columns('task')]
    if 'due_time' not in cols:
        default_dt = datetime.now() + timedelta(days=1)
        db.session.execute(text('ALTER TABLE task ADD COLUMN due_time DATETIME'))
        db.session.execute(text('UPDATE task SET due_time = :dt'), {'dt': default_dt})
        db.session.commit()
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.due_time).all()
    now = datetime.now()
    for task in tasks:
        diff = task.due_time - now
        task.allow_toggle = 0 <= diff.total_seconds() <= 3600
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    due_time_str = request.form['due_time']
    due_time = datetime.strptime(due_time_str, '%Y-%m-%dT%H:%M')
    task = Task(title=title, due_time=due_time)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    task = Task.query.get_or_404(task_id)
    task.title = request.form.get('title', task.title)
    if 'due_time' in request.form and request.form['due_time']:
        task.due_time = datetime.strptime(request.form['due_time'], '%Y-%m-%dT%H:%M')
    task.completed = 'completed' in request.form
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    task = Task.query.get_or_404(task_id)
    now = datetime.now()
    diff = task.due_time - now
    if 0 <= diff.total_seconds() <= 3600:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
