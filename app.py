from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Create Flask app instance
app = Flask(__name__)

# Create SQLite database instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Define model of a to-do list TASK object
class Task(db.Model):
    # db.Column represents a col in the database
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    # add DateTime column later

# Flask route to display all tasks
@app.route('/', methods=['GET', 'POST'])
def index(): 
    # Add new Task to database
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)
        # Put new Task in database
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding task!'
    # Select all Tasks from database
    all_tasks = Task.query.all()
    return render_template('index.html', tasks=all_tasks)

# Create the database in the main method
if __name__ == '__main__': 
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)