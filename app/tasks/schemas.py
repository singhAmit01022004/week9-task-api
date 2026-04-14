from app.extensions import ma
from app.models import Task

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True  # Include user_id
        load_instance = True # Useful for deserialization

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)