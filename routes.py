from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, Job, User

jobs_bp = Blueprint('jobs', __name__)
auth_bp = Blueprint('auth', __name__)

def check_employer_role():
    claims = get_jwt()
    if claims.get('role') != 'employer':
        return jsonify({'error': 'Access denied. Employer role required.'}), 403
    return None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  # 'employer' or 'job_seeker'

    if not username or not password or not role:
        return jsonify({'error': 'Username, password, and role are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    from flask_jwt_extended import create_access_token

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=username, additional_claims={'role': user.role})
    return jsonify({'access_token': access_token}), 200

@jobs_bp.route('/jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    jobs = Job.query.all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'location': job.location,
        'salary': job.salary,
        'job_type': job.job_type,
        'employer_id': job.employer_id
    } for job in jobs])

@jobs_bp.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    error = check_employer_role()
    if error:
        return error

    data = request.get_json()
    required_fields = ['title', 'description', 'location', 'salary', 'job_type', 'employer_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    if not isinstance(data['salary'], (int, float)) or data['salary'] <= 0:
        return jsonify({'error': 'Salary must be a positive number'}), 400

    new_job = Job(
        title=data['title'],
        description=data['description'],
        location=data['location'],
        salary=data['salary'],
        job_type=data['job_type'],
        employer_id=data['employer_id']
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify({'message': 'Job created', 'id': new_job.id}), 201

@jobs_bp.route('/jobs/<int:job_id>', methods=['PATCH'])
@jwt_required()
def update_job(job_id):
    error = check_employer_role()
    if error:
        return error

    job = Job.query.get_or_404(job_id)
    data = request.get_json()

    if 'salary' in data and (not isinstance(data['salary'], (int, float)) or data['salary'] <= 0):
        return jsonify({'error': 'Salary must be a positive number'}), 400

    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    job.location = data.get('location', job.location)
    job.salary = data.get('salary', job.salary)
    job.job_type = data.get('job_type', job.job_type)
    job.employer_id = data.get('employer_id', job.employer_id)
    db.session.commit()
    return jsonify({'message': 'Job updated'})

@jobs_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    error = check_employer_role()
    if error:
        return error

    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Job deleted'})
