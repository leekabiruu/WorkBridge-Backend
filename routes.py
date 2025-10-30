from flask import Blueprint, request, jsonify
from models import db, Job

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['GET'])
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
def create_job():
    data = request.get_json()
    new_job = Job(
        title=data['title'],
        description=data['description'],
        location=data['location'],
        salary=data['salary'],
        job_type=data['job_type'],
        employer_id=data['employer_id']  # Note: Employer auth not implemented
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify({'message': 'Job created', 'id': new_job.id}), 201

@jobs_bp.route('/jobs/<int:job_id>', methods=['PATCH'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.get_json()
    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    job.location = data.get('location', job.location)
    job.salary = data.get('salary', job.salary)
    job.job_type = data.get('job_type', job.job_type)
    job.employer_id = data.get('employer_id', job.employer_id)  # Note: Employer auth not implemented
    db.session.commit()
    return jsonify({'message': 'Job updated'})

@jobs_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Job deleted'})
