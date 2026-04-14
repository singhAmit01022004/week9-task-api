from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task
from app.extensions import db
from .schemas import task_schema, tasks_schema

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    
    # Filtering
    status = request.args.get('status')
    # Pagination
    page = request.args.get('page', 1, type=int)
    
    query = Task.query.filter_by(user_id=user_id)
    
    if status:
        query = query.filter_by(status=status)
        
    # Sorting (by due_date)
    query = query.order_by(Task.due_date.asc())
    
    paginated_results = query.paginate(page=page, per_page=5)
    return jsonify({
        "tasks": tasks_schema.dump(paginated_results.items),
        "total_pages": paginated_results.pages,
        "current_page": paginated_results.page
    }), 200

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        user_id=user_id
    )
    db.session.add(new_task)
    db.session.commit()
    return task_schema.dump(new_task), 201