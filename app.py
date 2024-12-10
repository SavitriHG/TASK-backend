
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "https://task-assignment-peach.vercel.app/"}})


# Configure the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://shavu:savitri@localhost/sales_log'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    entity_name = db.Column(db.String(100), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False)

# Initialize the database (create tables if they don't exist)
with app.app_context():
    db.create_all()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'date': task.date,
        'entityName': task.entity_name,
        'taskType': task.task_type,
        'time': task.time,
        'contactPerson': task.contact_person,
        'notes': task.notes,
        'status': task.status,
    } for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(
        date=data.get('date'),
        entity_name=data['entityName'],
        task_type=data['taskType'],
        time=data.get('time'),
        contact_person=data['contactPerson'],
        notes=data.get('notes', ''),
        status=data.get('status', 'Open'),
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully!', 'taskId': new_task.id}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = Task.query.get_or_404(task_id)
    task.date = data.get('date', task.date)
    task.entity_name = data.get('entityName', task.entity_name)
    task.task_type = data.get('taskType', task.task_type)
    task.time = data.get('time', task.time)
    task.contact_person = data.get('contactPerson', task.contact_person)
    task.notes = data.get('notes', task.notes)
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully!'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)